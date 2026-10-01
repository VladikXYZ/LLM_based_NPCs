SHARED_RPG_RULE = "You are a fantasy RPG NPC. Speak ONLY pure dialogue with NO stage directions, actions, or asterisks. Be direct and terse. Answer the player's exact question and immediately stop talking. Do NOT volunteer background facts unless directly asked, and do NOT over-explain. Treat your reality as a normal fantasy world. Maximum length: 2 short sentences."

# Mini reasoning: the NPC writes a short plan, the separator and then what it says.
# The separator is a single token in the tokenizers of the models.
MINI_SEPARATOR = "|"
MINI_REASONING_RULE = ("OUTPUT FORMAT, mandatory in every reply: "
                       "First write a brief response plan (at most two sentences), "
                       f"then exactly one {MINI_SEPARATOR} separator, then the spoken dialogue. "
                       f"Format: Brief response plan {MINI_SEPARATOR} Spoken dialogue. "
                       f"The plan is not spoken: the dialogue-only and length rules apply to the text after {MINI_SEPARATOR}.")

REASONING_SHARED_RPG_RULE = SHARED_RPG_RULE + " " + MINI_REASONING_RULE

# One entry per prompt format. Every template is built from these pieces:
#   system     - (open, close) around "<npc system message>\n\n<shared rule>"
#   user       - (open, close) around a user message
#   assistant  - generation prompt; it is also what precedes every past assistant message
#   end        - what closes a past assistant message
#   eos        - stop string
# The BOS token is not part of a family: utils adds it for the models that want one.
# The model's own reasoning is never used: the "assistant" prefix switches it off (empty think block),
# in the normal and in the mini reasoning templates alike.
# The prefix is also used for past assistant messages, so every new prompt starts with exactly
# the tokens that are already in the KV cache (prompt + generated reply).
FAMILIES = {
    # Qwen3.5, Qwen3.6, Bonsai, maple, MiniCPM5, LFM2.5-2.6B, Nemotron 3.5 Lightning, Nemotron3 Nano, granite 4.2
    "chatml": {
        "system": ("<|im_start|>system\n", "<|im_end|>\n"),
        "user": ("<|im_start|>user\n", "<|im_end|>\n"),
        "assistant": "<|im_start|>assistant\n<think>\n\n</think>\n\n",
        "end": "<|im_end|>\n",
        "eos": "<|im_end|>",
    },
    # LFM2, LFM2.5 without reasoning (no think block)
    "chatml_nr": {
        "system": ("<|im_start|>system\n", "<|im_end|>\n"),
        "user": ("<|im_start|>user\n", "<|im_end|>\n"),
        "assistant": "<|im_start|>assistant\n",
        "end": "<|im_end|>\n",
        "eos": "<|im_end|>",
    },
    # Nemotron Nano 9B v2
    "nemotron_v2": {
        "system": ("<SPECIAL_10>System\n", "\n"),
        "user": ("<SPECIAL_11>User\n", "\n"),
        "assistant": "<SPECIAL_11>Assistant\n<think></think>",
        "end": "\n<SPECIAL_12>\n",
        "eos": "<SPECIAL_12>",
    },
    "llama": {
        "system": ("<|start_header_id|>system<|end_header_id|>\n\n", "<|eot_id|>"),
        "user": ("<|start_header_id|>user<|end_header_id|>\n\n", "<|eot_id|>"),
        "assistant": "<|start_header_id|>assistant<|end_header_id|>\n\n",
        "end": "<|eot_id|>",
        "eos": "<|eot_id|>",
    },
    # gemma 4
    "gemma": {
        "system": ("<|turn>system\n", "<turn|>\n"),
        "user": ("<|turn>user\n", "<turn|>\n"),
        "assistant": "<|turn>model\n",
        "end": "<turn|>\n",
        "eos": "<turn|>",
    },
    # Ministral 3
    "mistral": {
        "system": ("[SYSTEM_PROMPT]", "[/SYSTEM_PROMPT]"),
        "user": ("[INST]", "[/INST]"),
        "assistant": "",
        "end": "</s>",
        "eos": "</s>",
    },
    # GLM 4.7 Flash, GLM 4.6V Flash
    "glm": {
        "system": ("[gMASK]<sop><|system|>", ""),
        "user": ("<|user|>", ""),
        "assistant": "<|assistant|><think></think>",
        "end": "",
        "eos": "<|user|>",
    },
    "ling": {
        "system": ("<role>SYSTEM</role>", "\ndetailed thinking off<|role_end|>"),
        "user": ("<role>HUMAN</role>", "<|role_end|>"),
        "assistant": "<role>ASSISTANT</role>\n<think></think>",
        "end": "<|role_end|>",
        "eos": "<|role_end|>",
    },
    "spark": {
        "system": ("<｜start▁of▁sentence｜><|System|>\n", "<｜end▁of▁sentence｜>"),
        "user": ("<｜start▁of▁sentence｜><|User|>", "<｜end▁of▁sentence｜>"),
        "assistant": "<｜start▁of▁sentence｜><|Bot|></think>",
        "end": "<｜end▁of▁sentence｜>",
        "eos": "<｜end▁of▁sentence｜>",
    },
    # gpt-oss (harmony): the analysis channel is skipped by opening the final channel directly
    "gptoss": {
        "system": ("<|start|>system<|message|>You are ChatGPT, a large language model trained by OpenAI.\n"
                   "Knowledge cutoff: 2024-06\n\nReasoning: low\n\n"
                   "# Valid channels: analysis, commentary, final. Channel must be included for every message.<|end|>"
                   "<|start|>developer<|message|># Instructions\n\n", "<|end|>"),
        "user": ("<|start|>user<|message|>", "<|end|>"),
        "assistant": "<|start|>assistant<|channel|>final<|message|>",
        "end": "<|end|>",
        "eos": "<|return|>",
    },
}

_SYSTEM = """{{- bos_token -}}
{%- if messages and messages[0].role == 'system' -%}
    {{- __SYS_OPEN__ + messages[0].content + '\\n\\n' + __RULE__ + __SYS_CLOSE__ -}}
{%- else -%}
    {{- __SYS_OPEN__ + __RULE__ + __SYS_CLOSE__ -}}
{%- endif -%}
"""

_TURNS = """{%- for message in messages -%}
    {%- if message.role == 'user' -%}
        {{- __USER_OPEN__ + message.content + __USER_CLOSE__ -}}
    {%- elif message.role == 'assistant' -%}
        {{- __ASSISTANT__ + message.content + __END__ -}}
    {%- endif -%}
{%- endfor -%}
{{- __ASSISTANT__ -}}
"""


def _build(template, family, rule):
    values = {
        "__RULE__": rule,
        "__SYS_OPEN__": family["system"][0], "__SYS_CLOSE__": family["system"][1],
        "__USER_OPEN__": family["user"][0], "__USER_CLOSE__": family["user"][1],
        "__ASSISTANT__": family["assistant"], "__END__": family["end"],
    }
    for key, value in values.items():
        template = template.replace(key, repr(value))
    return template


TEMPLATES_INFERENCE = {name: _build(_SYSTEM + _TURNS, f, SHARED_RPG_RULE) for name, f in FAMILIES.items()}
REASONING_TEMPLATES_INFERENCE = {name: _build(_SYSTEM + _TURNS, f, REASONING_SHARED_RPG_RULE) for name, f in FAMILIES.items()}

# Warmup renders only the system block, so the KV cache holds a prefix of every later prompt.
TEMPLATES_WARMUP = {name: _build(_SYSTEM, f, SHARED_RPG_RULE) for name, f in FAMILIES.items()}
REASONING_TEMPLATES_WARMUP = {name: _build(_SYSTEM, f, REASONING_SHARED_RPG_RULE) for name, f in FAMILIES.items()}

INFERENCE_TYPES = [TEMPLATES_INFERENCE, REASONING_TEMPLATES_INFERENCE]
WARMUP_TYPES = [TEMPLATES_WARMUP, REASONING_TEMPLATES_WARMUP]

EOS_TOKENS = {name: f["eos"] for name, f in FAMILIES.items()}
