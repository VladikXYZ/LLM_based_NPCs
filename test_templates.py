"""Checks of the custom chat templates. Needs no model: run `python test_templates.py` (or pytest)."""
import json

from jinja2.sandbox import ImmutableSandboxedEnvironment

import chat_templates as ct

ENV = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
SYSTEM = {"role": "system", "content": "You are Garrick."}
TURNS = [("Hello", "Greetings."), ("What do you sell?", "Swords."), ("How much?", "Ten gold.")]


def render(template, messages, family):
    return ENV.from_string(template).render(messages=messages, bos_token="<BOS>")


def test_every_model_has_a_template():
    with open("data/models.json") as f:
        for model in json.load(f):
            family = model["family"]
            assert family is None or family in ct.FAMILIES, model


def test_kv_cache_prefix():
    """What the KV cache holds after a turn (prompt + reply) must be the start of the next prompt.

    This is the Qwen bug: the prompt ended with an empty think block that was missing from the history,
    so no later prompt matched the cache and the whole conversation was evaluated again on every turn.
    """
    for reason in (0, 1):
        for family in ct.FAMILIES:
            template = ct.INFERENCE_TYPES[reason][family]
            warmup = render(ct.WARMUP_TYPES[reason][family], [SYSTEM], family)
            messages, cached = [SYSTEM], warmup
            for question, answer in TURNS:
                messages.append({"role": "user", "content": question})
                prompt = render(template, messages, family)
                assert prompt.startswith(cached), (family, reason, cached, prompt)
                cached = prompt + answer
                messages.append({"role": "assistant", "content": answer})


def test_rule_is_in_the_system_block():
    for reason, rule in enumerate((ct.SHARED_RPG_RULE, ct.REASONING_SHARED_RPG_RULE)):
        for family in ct.FAMILIES:
            prompt = render(ct.INFERENCE_TYPES[reason][family], [SYSTEM, {"role": "user", "content": "Hello"}], family)
            assert prompt.count(rule) == 1 and "You are Garrick.\n\n" + rule in prompt, family
            assert prompt.startswith("<BOS>"), family
            # without a system message the rule is still there
            assert rule in render(ct.INFERENCE_TYPES[reason][family], [{"role": "user", "content": "Hello"}], family)


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
