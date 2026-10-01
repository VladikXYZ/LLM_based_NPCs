"""Checks of the custom chat templates. Needs no model: run `python test_templates.py` (or pytest)."""
import json

from jinja2.sandbox import ImmutableSandboxedEnvironment

import chat_templates as ct

ENV = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
SYSTEM = {"role": "system", "content": "You are Garrick."}
TURNS = [("Hello", "Greetings."), ("What do you sell?", "Swords."), ("How much?", "Ten gold.")]


def render(family, reason, messages, add_generation_prompt=True):
    entry = ct.TEMPLATES[family]
    return ENV.from_string(entry["template"][reason]).render(
        messages=messages, bos_token=entry["bos"], add_generation_prompt=add_generation_prompt)


def test_every_model_has_a_template():
    with open("data/models.json") as f:
        for model in json.load(f):
            family = model["family"]
            assert family is None or family in ct.TEMPLATES, model


def test_kv_cache_prefix():
    """What the KV cache holds after a turn (prompt + reply) must be the start of the next prompt.

    This is the Qwen bug: the prompt ended with an empty think block that was missing from the history,
    so no later prompt matched the cache and the whole conversation was evaluated again on every turn.
    """
    for reason in (0, 1):
        for family in ct.TEMPLATES:
            warmup = render(family, reason, [SYSTEM], add_generation_prompt=False)
            messages, cached = [SYSTEM], warmup
            for question, answer in TURNS:
                messages.append({"role": "user", "content": question})
                prompt = render(family, reason, messages)
                assert prompt.startswith(cached), (family, reason, cached, prompt)
                cached = prompt + answer
                messages.append({"role": "assistant", "content": answer})


def test_rule_is_in_the_system_block():
    for reason, rule in enumerate((ct.SHARED_RPG_RULE, ct.REASONING_SHARED_RPG_RULE)):
        for family, entry in ct.TEMPLATES.items():
            prompt = render(family, reason, [SYSTEM, {"role": "user", "content": "Hello"}])
            assert prompt.count(rule) == 1 and "You are Garrick.\n\n" + rule in prompt, family
            assert prompt.startswith(entry["bos"]) and entry["eos"], family
            # without a system message the rule is still there
            assert rule in render(family, reason, [{"role": "user", "content": "Hello"}])


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
