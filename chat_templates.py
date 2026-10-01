SHARED_RPG_RULE = "You are a fantasy RPG NPC. Speak ONLY pure dialogue with NO stage directions, actions, or asterisks. Be direct and terse. Answer the player's exact question and immediately stop talking. Do NOT volunteer background facts unless directly asked, and do NOT over-explain. Treat your reality as a normal fantasy world. Maximum length: 2 short sentences."

# Mini reasoning: the NPC writes a short plan, the separator and then what it says.
MINI_REASONING_RULE = ("OUTPUT FORMAT, mandatory in every reply: "
                       "First write a brief response plan (at most two sentences), "
                       "then exactly one <speech> separator, then the spoken dialogue. "
                       "Format: Brief response plan <speech> Spoken dialogue. "
                       "The plan is not spoken: the dialogue-only and length rules apply to the text after <speech>.")

REASONING_SHARED_RPG_RULE = SHARED_RPG_RULE + " " + MINI_REASONING_RULE

# False switches the model's own <think> phase off in mini reasoning mode as well (the plan replaces it).
# True leaves it on: Qwen then thinks instead of writing the plan and fails the format.
MINI_NATIVE_THINKING = False

# One entry per prompt format. Every template is built from these pieces:
#   bos        - True if the model's own template starts with its BOS token
#   system     - (open, close) around "<npc system message>\n\n<shared rule>"
#   user       - (open, close) around a user message
#   assistant  - generation prompt; it is also what precedes every past assistant message
#   end        - what closes a past assistant message
#   eos        - stop string
#   thinking   - optional overrides of the pieces above for the reasoning templates
# Normal templates switch native thinking off through the "assistant" prefix (empty think block).
# Reasoning templates do the same, unless MINI_NATIVE_THINKING is True: then the "thinking" overrides apply.
# The prefix is also used for past assistant messages, so every new prompt starts with exactly
# the tokens that are already in the KV cache (prompt + generated reply).
FAMILIES = {
    # Qwen3.5, Qwen3.6, Bonsai, maple
    "chatml": {
        "bos": False,
        "system": ("<|im_start|>system\n", "<|im_end|>\n"),
        "user": ("<|im_start|>user\n", "<|im_end|>\n"),
        "assistant": "<|im_start|>assistant\n<think>\n\n</think>\n\n",
        "end": "<|im_end|>\n",
        "eos": "<|im_end|>",
        "thinking": {"assistant": "<|im_start|>assistant\n"},
    },
    # MiniCPM5, LFM2.5-2.6B (chatml with BOS and a think block)
    "chatml_bos": {
        "bos": True,
        "system": ("<|im_start|>system\n", "<|im_end|>\n"),
        "user": ("<|im_start|>user\n", "<|im_end|>\n"),
        "assistant": "<|im_start|>assistant\n<think>\n\n</think>\n\n",
        "end": "<|im_end|>\n",
        "eos": "<|im_end|>",
        "thinking": {"assistant": "<|im_start|>assistant\n"},
    },
    # LFM2, LFM2.5 without reasoning (chatml with BOS, no think block)
    "chatml_nr": {
        "bos": True,
        "system": ("<|im_start|>system\n", "<|im_end|>\n"),
        "user": ("<|im_start|>user\n", "<|im_end|>\n"),
        "assistant": "<|im_start|>assistant\n",
        "end": "<|im_end|>\n",
        "eos": "<|im_end|>",
    },
    # Nemotron 3.5 Lightning, Nemotron3 Nano, granite 4.2 (chatml, think block without newlines)
    "chatml_inline": {
        "bos": False,
        "system": ("<|im_start|>system\n", "<|im_end|>\n"),
        "user": ("<|im_start|>user\n", "<|im_end|>\n"),
        "assistant": "<|im_start|>assistant\n<think></think>",
        "end": "<|im_end|>\n",
        "eos": "<|im_end|>",
        "thinking": {"assistant": "<|im_start|>assistant\n"},
    },
    # Nemotron Nano 9B v2
    "nemotron_v2": {
        "bos": False,
        "system": ("<SPECIAL_10>System\n", "\n"),
        "user": ("<SPECIAL_11>User\n", "\n"),
        "assistant": "<SPECIAL_11>Assistant\n<think></think>",
        "end": "\n<SPECIAL_12>\n",
        "eos": "<SPECIAL_12>",
        "thinking": {"assistant": "<SPECIAL_11>Assistant\n"},
    },
    "llama": {
        "bos": True,
        "system": ("<|start_header_id|>system<|end_header_id|>\n\n", "<|eot_id|>"),
        "user": ("<|start_header_id|>user<|end_header_id|>\n\n", "<|eot_id|>"),
        "assistant": "<|start_header_id|>assistant<|end_header_id|>\n\n",
        "end": "<|eot_id|>",
        "eos": "<|eot_id|>",
    },
    # gemma 4 E2B, E4B
    "gemma": {
        "bos": True,
        "system": ("<|turn>system\n", "<turn|>\n"),
        "user": ("<|turn>user\n", "<turn|>\n"),
        "assistant": "<|turn>model\n",
        "end": "<turn|>\n",
        "eos": "<turn|>",
    },
    # gemma 4 12b, 26B (empty thought channel)
    "gemma_think": {
        "bos": True,
        "system": ("<|turn>system\n", "<turn|>\n"),
        "user": ("<|turn>user\n", "<turn|>\n"),
        "assistant": "<|turn>model\n<|channel>thought\n<channel|>",
        "end": "<turn|>\n",
        "eos": "<turn|>",
        "thinking": {"assistant": "<|turn>model\n"},
    },
    # Ministral 3
    "mistral": {
        "bos": True,
        "system": ("[SYSTEM_PROMPT]", "[/SYSTEM_PROMPT]"),
        "user": ("[INST]", "[/INST]"),
        "assistant": "",
        "end": "</s>",
        "eos": "</s>",
    },
    # GLM 4.7 Flash
    "glm": {
        "bos": False,
        "system": ("[gMASK]<sop><|system|>", ""),
        "user": ("<|user|>", ""),
        "assistant": "<|assistant|></think>",
        "end": "",
        "eos": "<|user|>",
        "thinking": {"assistant": "<|assistant|>"},
    },
    # GLM 4.6V Flash
    "glm_v": {
        "bos": False,
        "system": ("[gMASK]<sop><|system|>\n", ""),
        "user": ("<|user|>\n", "/nothink"),
        "assistant": "<|assistant|>\n<think></think>\n",
        "end": "",
        "eos": "<|user|>",
        "thinking": {"assistant": "<|assistant|>\n", "user": ("<|user|>\n", "")},
    },
    "ling": {
        "bos": False,
        "system": ("<role>SYSTEM</role>", "\ndetailed thinking off<|role_end|>"),
        "user": ("<role>HUMAN</role>", "<|role_end|>"),
        "assistant": "<role>ASSISTANT</role>\n<think></think>",
        "end": "<|role_end|>",
        "eos": "<|role_end|>",
        "thinking": {"assistant": "<role>ASSISTANT</role>\n", "system": ("<role>SYSTEM</role>", "\ndetailed thinking on<|role_end|>")},
    },
    "spark": {
        "bos": False,
        "system": ("<｜start▁of▁sentence｜><|System|>\n", "<｜end▁of▁sentence｜>"),
        "user": ("<｜start▁of▁sentence｜><|User|>", "<｜end▁of▁sentence｜>"),
        "assistant": "<｜start▁of▁sentence｜><|Bot|></think>",
        "end": "<｜end▁of▁sentence｜>",
        "eos": "<｜end▁of▁sentence｜>",
        "thinking": {"assistant": "<｜start▁of▁sentence｜><|Bot|>"},
    },
    # gpt-oss (harmony): the analysis channel is skipped by opening the final channel directly
    "gptoss": {
        "bos": False,
        "system": ("<|start|>system<|message|>You are ChatGPT, a large language model trained by OpenAI.\n"
                   "Knowledge cutoff: 2024-06\n\nReasoning: low\n\n"
                   "# Valid channels: analysis, commentary, final. Channel must be included for every message.<|end|>"
                   "<|start|>developer<|message|># Instructions\n\n", "<|end|>"),
        "user": ("<|start|>user<|message|>", "<|end|>"),
        "assistant": "<|start|>assistant<|channel|>final<|message|>",
        "end": "<|end|>",
        "eos": "<|return|>",
        "thinking": {"assistant": "<|start|>assistant"},
    },
    "phi": {
        "bos": False,
        "system": ("<|system|>", "<|end|>"),
        "user": ("<|user|>", "<|end|>"),
        "assistant": "<|assistant|>",
        "end": "<|end|>",
        "eos": "<|end|>",
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


def _build(template, family, rule, thinking=False):
    if thinking:
        family = {**family, **family.get("thinking", {})}
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
REASONING_TEMPLATES_INFERENCE = {name: _build(_SYSTEM + _TURNS, f, REASONING_SHARED_RPG_RULE, MINI_NATIVE_THINKING) for name, f in FAMILIES.items()}

# Warmup renders only the system block, so the KV cache holds a prefix of every later prompt.
TEMPLATES_WARMUP = {name: _build(_SYSTEM, f, SHARED_RPG_RULE) for name, f in FAMILIES.items()}
REASONING_TEMPLATES_WARMUP = {name: _build(_SYSTEM, f, REASONING_SHARED_RPG_RULE, MINI_NATIVE_THINKING) for name, f in FAMILIES.items()}

INFERENCE_TYPES = [TEMPLATES_INFERENCE, REASONING_TEMPLATES_INFERENCE]
WARMUP_TYPES = [TEMPLATES_WARMUP, REASONING_TEMPLATES_WARMUP]

EOS_TOKENS = {name: f["eos"] for name, f in FAMILIES.items()}
BOS_FAMILIES = {name for name, f in FAMILIES.items() if f["bos"]}
