"""Tries several reply prefixes on one model and prints what the model answers after each of them.

    python probe_prefix.py [device] [part of the model name]      e.g. python probe_prefix.py 0 "Lythri 7B"

Use it for a model that keeps reasoning: the prefix whose replies are plain dialogue goes into vlad_temps.py.
"""
import os
import sys

from llama_cpp import Llama
from llama_cpp.llama_chat_format import Jinja2ChatFormatter

import utils
from utils import SHARED_RPG_RULE, REASONING_RULE, NPC, TEMPLATES, get_devices, get_models

MAX_TOKENS = 64
QUESTIONS = ["Where can I find the nearest blacksmith in this town?",
             "I need a healing potion. What is your best price?",
             "I just arrived from the capital, and the journey was fraught with perilous encounters. Bandits ambushed us "
             "near the river crossing. Do you know if the local guard is planning to secure the main trade routes anytime soon?"]
# what the template writes right after the model's turn opens (and in front of every past reply)
PREFIXES = {
    "none": "",
    "empty think, newlines": "<think>\n\n</think>\n\n",
    "empty think, one newline": "<think>\n</think>\n\n",
    "empty think, inline": "<think></think>",
    "short fixed thought": "<think>\nI answer as the NPC, directly and in one or two short sentences.\n</think>\n\n",
    "gemma thought channel": "<|channel>thought\n\n<channel|>",
}


def main(dev, wanted):
    device = get_devices()[dev]
    model = next(m for m in get_models() if wanted.lower() in m["name"].lower())
    os.environ["GGML_VK_VISIBLE_DEVICES"] = str(device["id"] * (device["type"] == "Vulkan"))
    if model["family"] not in ("gemma", "gemma_think", "lythri"): sys.exit(f"{model['name']}: only models with gemma turn markers are supported")
    family = TEMPLATES["gemma"]  # the plain template, the prefixes are added below
    print(f"{model['name']} on {device['name']}")
    with utils.Silencer():
        llm = Llama(model_path=model["path"], n_gpu_layers=-1 if device["type"] == "Vulkan" else 0, n_ctx=4096, verbose=False, seed=42)

    rule = f"{SHARED_RPG_RULE} {NPC['role']} {REASONING_RULE[0]}"
    opening = "'<|turn>model\n'"  # as it is written in the template, in both places where the model's turn starts
    assert family["template"].count(opening) == 2
    for name, prefix in PREFIXES.items():
        template = family["template"].replace(opening, opening[:-1] + prefix + "'").replace("__RULE__", f"\"{rule}\"")
        llm.chat_handler = Jinja2ChatFormatter(template=template, eos_token=family["eos"], bos_token=family["bos"]).to_chat_handler()
        llm.reset()
        history, clean = [], 0
        print(f"\n=== {name}: {prefix!r}")
        for question in QUESTIONS:
            history.append({"role": "user", "content": question})
            reply = llm.create_chat_completion(messages=history, max_tokens=MAX_TOKENS)["choices"][0]
            text = reply["message"]["content"]
            history.append({"role": "assistant", "content": text})
            ok = reply["finish_reason"] == "stop" and not any(tag in text for tag in ("<think>", "</think>", "channel", "*"))
            clean += ok
            print(f"   {'ok ' if ok else 'BAD'} {text.strip()[:200]!r}")
        print(f"   -> {clean}/{len(QUESTIONS)} replies are plain and end by themselves")
    llm.close()


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 0, sys.argv[2] if len(sys.argv) > 2 else "Lythri 7B")
