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

# The system block is all that is rendered when add_generation_prompt is False. That is the warmup:
# the KV cache then holds a prefix of every later prompt.
_TEMPLATE = """{{- bos_token -}}
{%- if messages and messages[0].role == 'system' -%}
    {{- __SYS_OPEN__ + messages[0].content + '\\n\\n' + __RULE__ + __SYS_CLOSE__ -}}
{%- else -%}
    {{- __SYS_OPEN__ + __RULE__ + __SYS_CLOSE__ -}}
{%- endif -%}
{%- if add_generation_prompt -%}
    {%- for message in messages -%}
        {%- if message.role == 'user' -%}
            {{- __USER_OPEN__ + message.content + __USER_CLOSE__ -}}
        {%- elif message.role == 'assistant' -%}
            {{- __ASSISTANT__ + message.content + __END__ -}}
        {%- endif -%}
    {%- endfor -%}
    {{- __ASSISTANT__ -}}
{%- endif -%}
"""


def _family(bos, eos, system, user, assistant, end):
    """Build one entry of TEMPLATES.

    system     - (open, close) around "<npc system message>\\n\\n<shared rule>"
    user       - (open, close) around a user message
    assistant  - generation prompt; it is also what precedes every past assistant message
    end        - what closes a past assistant message
    The model's own reasoning is never used: the "assistant" prefix switches it off (empty think block).
    The prefix is also used for past assistant messages, so every new prompt starts with exactly
    the tokens that are already in the KV cache (prompt + generated reply).
    """
    def build(rule):
        values = {
            "__RULE__": rule,
            "__SYS_OPEN__": system[0], "__SYS_CLOSE__": system[1],
            "__USER_OPEN__": user[0], "__USER_CLOSE__": user[1],
            "__ASSISTANT__": assistant, "__END__": end,
        }
        template = _TEMPLATE
        for key, value in values.items():
            template = template.replace(key, repr(value))
        return template

    return {"template": [build(SHARED_RPG_RULE), build(REASONING_SHARED_RPG_RULE)], "bos": bos, "eos": eos}


# family -> {"template": [inference, mini reasoning], "bos": BOS token ("" for none), "eos": stop string}
TEMPLATES = {
    # Qwen3.5, Qwen3.6, Bonsai, maple, MiniCPM5, LFM2.5-2.6B, Nemotron 3.5 Lightning, Nemotron3 Nano, granite 4.2
    "chatml": _family(
        bos="", eos="<|im_end|>",
        system=("<|im_start|>system\n", "<|im_end|>\n"),
        user=("<|im_start|>user\n", "<|im_end|>\n"),
        assistant="<|im_start|>assistant\n<think>\n\n</think>\n\n",
        end="<|im_end|>\n",
    ),
    # LFM2, LFM2.5 without reasoning (no think block)
    "chatml_nr": _family(
        bos="<|startoftext|>", eos="<|im_end|>",
        system=("<|im_start|>system\n", "<|im_end|>\n"),
        user=("<|im_start|>user\n", "<|im_end|>\n"),
        assistant="<|im_start|>assistant\n",
        end="<|im_end|>\n",
    ),
    # Nemotron Nano 9B v2
    "nemotron_v2": _family(
        bos="", eos="<SPECIAL_12>",
        system=("<SPECIAL_10>System\n", "\n"),
        user=("<SPECIAL_11>User\n", "\n"),
        assistant="<SPECIAL_11>Assistant\n<think></think>",
        end="\n<SPECIAL_12>\n",
    ),
    "llama": _family(
        bos="<|begin_of_text|>", eos="<|eot_id|>",
        system=("<|start_header_id|>system<|end_header_id|>\n\n", "<|eot_id|>"),
        user=("<|start_header_id|>user<|end_header_id|>\n\n", "<|eot_id|>"),
        assistant="<|start_header_id|>assistant<|end_header_id|>\n\n",
        end="<|eot_id|>",
    ),
    # gemma 4
    "gemma": _family(
        bos="<bos>", eos="<turn|>",
        system=("<|turn>system\n", "<turn|>\n"),
        user=("<|turn>user\n", "<turn|>\n"),
        assistant="<|turn>model\n",
        end="<turn|>\n",
    ),
    # Ministral 3
    "mistral": _family(
        bos="<s>", eos="</s>",
        system=("[SYSTEM_PROMPT]", "[/SYSTEM_PROMPT]"),
        user=("[INST]", "[/INST]"),
        assistant="",
        end="</s>",
    ),
    # GLM 4.7 Flash, GLM 4.6V Flash
    "glm": _family(
        bos="", eos="<|user|>",
        system=("[gMASK]<sop><|system|>", ""),
        user=("<|user|>", ""),
        assistant="<|assistant|><think></think>",
        end="",
    ),
    "ling": _family(
        bos="", eos="<|role_end|>",
        system=("<role>SYSTEM</role>", "\ndetailed thinking off<|role_end|>"),
        user=("<role>HUMAN</role>", "<|role_end|>"),
        assistant="<role>ASSISTANT</role>\n<think></think>",
        end="<|role_end|>",
    ),
    "spark": _family(
        bos="", eos="<｜end▁of▁sentence｜>",
        system=("<｜start▁of▁sentence｜><|System|>\n", "<｜end▁of▁sentence｜>"),
        user=("<｜start▁of▁sentence｜><|User|>", "<｜end▁of▁sentence｜>"),
        assistant="<｜start▁of▁sentence｜><|Bot|></think>",
        end="<｜end▁of▁sentence｜>",
    ),
    # gpt-oss (harmony): the analysis channel is skipped by opening the final channel directly
    "gptoss": _family(
        bos="", eos="<|return|>",
        system=("<|start|>system<|message|>You are ChatGPT, a large language model trained by OpenAI.\n"
                "Knowledge cutoff: 2024-06\n\nReasoning: low\n\n"
                "# Valid channels: analysis, commentary, final. Channel must be included for every message.<|end|>"
                "<|start|>developer<|message|># Instructions\n\n", "<|end|>"),
        user=("<|start|>user<|message|>", "<|end|>"),
        assistant="<|start|>assistant<|channel|>final<|message|>",
        end="<|end|>",
    ),
}


if __name__ == "__main__":
    # export the templates: python chat_templates.py
    import json
    with open("data/chat_templates.json", "w", encoding="utf-8") as f:
        json.dump(TEMPLATES, f, indent=1, ensure_ascii=False)
    print(f"Saved {len(TEMPLATES)} families to data/chat_templates.json")
