"""Talks to every model in models/ for a few turns, normal and mini reasoning, and prints what works.

    python check_models.py [device]

Columns of the final table:
    BOS     - ok: the prompt starts with the BOS token of the family; MISSING: it should but does not;
              WANTED: the family has none, yet the model asks for one
    REPLY   - normal mode: replies that are plain dialogue (not empty, no <think> or | in them)
    STOP    - normal mode: replies that ended by themselves, before MAX_TOKENS
    CACHE   - normal mode: turns whose prompt reused everything that was in the KV cache
    MINI    - mini reasoning: replies in the "plan | dialogue" format
    MCACHE  - mini reasoning: as CACHE, the first turn is skipped because the template has just changed
"""
import json
import os
import sys
import questionary

import utils
import npc_runtime
from chat_templates import MINI_REASONING_RULE, TEMPLATES
from utils import get_devices, get_models

RED = "\033[91m"
GREEN = "\033[92m"
GREY = "\033[90m"
RESET = "\033[0m"

CONTEXT_SIZE = 4096
MAX_TOKENS = 200
CUSTOM_JINJA = True
QUESTIONS = ["Hello, who are you?", "What do you want from me?", "Where do you live?"]
with open("data/data_3npcs.json") as file: NPC = json.load(file)[2]


def system_message(model, mini):
    # the custom templates add the rule themselves; the model's own template does not
    if CUSTOM_JINJA and model["family"]: content = NPC["role"]
    else: content = NPC["role"] + NPC["shared_system_prompt"] + (" " + MINI_REASONING_RULE if mini else "")
    return {"role": "system", "content": content}


def watch_cache(llm):
    """Record how many cached tokens are kept when a prompt is evaluated."""
    seen = {"reused": None}
    original = llm.eval

    def eval_tokens(tokens):
        if seen["reused"] is None: seen["reused"] = llm.n_tokens
        return original(tokens)

    llm.eval = eval_tokens
    return seen


def converse(llm, model, mini, cache):
    history = [system_message(model, mini)]
    turns = []
    for question in QUESTIONS:
        history.append({"role": "user", "content": question})
        cached, cache["reused"] = llm.n_tokens, None
        result = npc_runtime.generate(llm, history, mini, MAX_TOKENS)
        history.append({"role": "assistant", "content": result.raw})
        turns.append((result, cached > 0 and cache["reused"] == cached))
        shown = result.raw.replace("\n", " ")
        print(f"   {GREY}{question}{RESET} {shown[:150]}{'...' if len(shown) > 150 else ''}")
    return turns


def check(model, gpu_layers):
    row = {"MODEL": model["name"], "FAMILY": model["family"] or "own", "BOS": "-", "REPLY": "-", "STOP": "-",
           "CACHE": "-", "MINI": "-", "MCACHE": "-", "RESULT": "load failed"}
    llm = None
    llm_kwargs = {"model_path": model["path"], "n_gpu_layers": gpu_layers, "n_ctx": CONTEXT_SIZE,
                  "verbose": False, "temperature": 0}
    count = lambda values: f"{sum(values)}/{len(values)}"
    try:
        warmup = [system_message(model, False), {"role": "user", "content": "warmup"}]
        llm = utils.load_llm(model, llm_kwargs, warmup, CUSTOM_JINJA, reason=False, log=True)
        cache = watch_cache(llm)
        row["RESULT"] = "crashed"

        normal = converse(llm, model, False, cache)
        if CUSTOM_JINJA and model["family"]:
            starts_with_bos = llm._input_ids[0] == llm.token_bos()
            if TEMPLATES[model["family"]]["bos"]: row["BOS"] = "ok" if starts_with_bos else "MISSING"
            elif llm._model.add_bos_token() and not starts_with_bos: row["BOS"] = "WANTED"
        row["REPLY"] = count([result.format_ok for result, _ in normal])
        row["STOP"] = count([result.chunks < MAX_TOKENS for result, _ in normal])
        row["CACHE"] = count([hit for _, hit in normal])

        print(f"   {GREY}-- mini reasoning{RESET}")
        utils.set_reasoning(llm, model, CUSTOM_JINJA, True)
        mini = converse(llm, model, True, cache)
        row["MINI"] = count([result.format_ok for result, _ in mini])
        row["MCACHE"] = count([hit for _, hit in mini[1:]])

        full = f"{len(QUESTIONS)}/{len(QUESTIONS)}"
        good = row["REPLY"] == row["STOP"] == row["CACHE"] == full and row["BOS"] != "MISSING"
        row["RESULT"] = "ok" if good else "CHECK"
    except Exception as e:
        print(f"   {RED}{e}{RESET}")
    finally:
        if hasattr(llm, 'close'): llm.close()
        del llm
    return row


def main(dev=None):
    devices = get_devices()
    models = get_models()
    if not models: sys.exit(f"{RED}No models found in the models directory!{RESET}")

    if dev is None:
        device_choices = [f"{i} | {d['type']:<8} | {d['name']}" for i, d in enumerate(devices)]
        dev_choice = questionary.select("Select device:", choices=device_choices, qmark="🎮").ask()
        if not dev_choice: sys.exit("Exiting...")
        dev = int(dev_choice.split("|")[0])
    if not 0 <= dev < len(devices): sys.exit(f"Invalid device value:{dev}")
    device = devices[dev]

    print(f"\nChecking {len(models)} models on {device['name']}...")
    gpu_layers = -1 if device["type"] == "Vulkan" else 0
    os.environ["GGML_VK_VISIBLE_DEVICES"] = str(device["id"] * (device["type"] == "Vulkan"))

    rows = [check(model, gpu_layers) for model in models]

    header = list(rows[0])
    widths = [max(len(str(row[key])) for row in rows + [dict(zip(header, header))]) for key in header]
    print("\n" + "  ".join(key.ljust(width) for key, width in zip(header, widths)))
    for row in rows:
        colour = GREEN if row["RESULT"] == "ok" else RED
        print(colour + "  ".join(str(row[key]).ljust(width) for key, width in zip(header, widths)) + RESET)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) == 2 else None)
