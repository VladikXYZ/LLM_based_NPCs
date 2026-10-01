shared_prompt = "You are a fantasy RPG NPC. Speak ONLY pure dialogue with NO stage directions, actions, or asterisks. Be direct and terse. Answer the player's exact question and immediately stop talking. Do NOT volunteer background facts unless directly asked, and do NOT over-explain. Treat your reality as a normal fantasy world. Maximum length: 2 short sentences."

shared_prompt_reasoning = shared_prompt + " FORMAT REQUIREMENT: You MUST prepend your dialogue with a brief internal thought (max 2 sentences) followed by exactly ONE '<speech>' separator. Example format: Internal thought <speech> Spoken dialogue."

# Base template strings with placeholder __RULE__
chatml_nt_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<|im_start|>system\n" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "<|im_end|>\n" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<|im_start|>system\n" + shared_prompt + "<|im_end|>\n" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<|im_start|>user\n" + message.content + "<|im_end|>\n" -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<|im_start|>assistant\n" + message.content + "<|im_end|>\n" -}}
    {%- endif -%}
{%- endfor -%}"""

chatml_thinking_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<|im_start|>system\n" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "<|im_end|>\n" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<|im_start|>system\n" + shared_prompt + "<|im_end|>\n" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<|im_start|>user\n" + message.content + "<|im_end|>\n" -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<|im_start|>assistant\n<think></think>\n" + message.content + "<|im_end|>\n" -}}
    {%- endif -%}
{%- endfor -%}"""

llama3_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<|start_header_id|>system<|end_header_id|>\n\n" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "<|eot_id|>" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<|start_header_id|>system<|end_header_id|>\n\n" + shared_prompt + "<|eot_id|>" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<|start_header_id|>user<|end_header_id|>\n\n" + message.content + "<|eot_id|>" -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<|start_header_id|>assistant<|end_header_id|>\n\n" + message.content + "<|eot_id|>" -}}
    {%- endif -%}
{%- endfor -%}"""

gemma4_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<|turn>system\n" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "<turn|>\n" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<|turn>system\n" + shared_prompt + "<turn|>\n" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<|turn>user\n" + message.content + "<turn|>\n" -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<|turn>model\n" + message.content + "<turn|>\n" -}}
    {%- endif -%}
{%- endfor -%}"""

ministral3_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "[SYSTEM_PROMPT]" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "[/SYSTEM_PROMPT]" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "[SYSTEM_PROMPT]" + shared_prompt + "[/SYSTEM_PROMPT]" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "[INST]" + message.content + "[/INST]" -}}
    {%- elif message.role == 'assistant' -%}
        {{- message.content + "</s>" -}}
    {%- endif -%}
{%- endfor -%}"""

glm4_base = r"""{%- set shared_prompt = __RULE__ -%}
[gMASK]<sop>
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<|system|>\n" + shared_prompt + "\n\nNPC Persona:\n" + message.content -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<|system|>\n" + shared_prompt -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<|user|>\n" + message.content -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<|assistant|>\n" + message.content -}}
    {%- endif -%}
{%- endfor -%}"""

gpt_oss_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<|start|>system<|message|>" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "<|end|>" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<|start|>system<|message|>" + shared_prompt + "<|end|>" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<|start|>user<|message|>" + message.content + "<|end|>" -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<|start|>assistant<|channel|>final<|message|>" + message.content + "<|end|>" -}}
    {%- endif -%}
{%- endfor -%}"""

spark_x2_5_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<｜start▁of▁sentence｜><|System|>\n" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "<｜end▁of▁sentence｜>" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<｜start▁of▁sentence｜><|System|>\n" + shared_prompt + "<｜end▁of▁sentence｜>" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<｜start▁of▁sentence｜><|User|>" + message.content + "<｜end▁of▁sentence｜>" -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<｜start▁of▁sentence｜><|Bot|>" + message.content + "<｜end▁of▁sentence｜>" -}}
    {%- endif -%}
{%- endfor -%}"""

ling_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<role>SYSTEM</role>" + shared_prompt + "\n\nNPC Persona:\n" + message.content + "<|role_end|>" -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<role>SYSTEM</role>" + shared_prompt + "<|role_end|>" -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "<role>HUMAN</role>" + message.content + "<|role_end|>" -}}
    {%- elif message.role == 'assistant' -%}
        {{- "<role>ASSISTANT</role>\n<think></think>\n" + message.content + "<|role_end|>" -}}
    {%- endif -%}
{%- endfor -%}"""

nemotron_base = r"""{%- set shared_prompt = __RULE__ -%}
{%- set ns = namespace(system_printed=false) -%}
{%- for message in messages -%}
    {%- if message.role == 'system' -%}
        {{- "<SPECIAL_10>System\n" + shared_prompt + "\n\nNPC Persona:\n" + message.content -}}
        {%- set ns.system_printed = true -%}
    {%- elif message.role == 'user' -%}
        {%- if not ns.system_printed -%}
            {{- "<SPECIAL_10>System\n" + shared_prompt -}}
            {%- set ns.system_printed = true -%}
        {%- endif -%}
        {{- "\n<SPECIAL_11>User\n" + message.content -}}
    {%- elif message.role == 'assistant' -%}
        {{- "\n<SPECIAL_11>Assistant\n" + message.content + "\n<SPECIAL_12>" -}}
    {%- endif -%}
{%- endfor -%}"""


# The combined overarching dictionary
npc_templates = {
    "ChatML_Non_Thinking": {
        "bos": "<|im_start|>",
        "eos": "<|im_end|>",
        "special_separator": "<|im_start|>",
        "inference_templates": [
            chatml_nt_base.replace("__RULE__", repr(shared_prompt)),
            chatml_nt_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "ChatML_Thinking": {
        "bos": "<|im_start|>",
        "eos": "<|im_end|>",
        "special_separator": "<|im_start|>",
        "inference_templates": [
            chatml_thinking_base.replace("__RULE__", repr(shared_prompt)),
            chatml_thinking_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "Llama_3": {
        "bos": "<|begin_of_text|>",
        "eos": "<|eot_id|>",
        "special_separator": "<|start_header_id|>",
        "inference_templates": [
            llama3_base.replace("__RULE__", repr(shared_prompt)),
            llama3_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "Gemma_4": {
        "bos": "<bos>",
        "eos": "<turn|>",
        "special_separator": "<|turn>",
        "inference_templates": [
            gemma4_base.replace("__RULE__", repr(shared_prompt)),
            gemma4_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "Ministral_3": {
        "bos": "<s>",
        "eos": "</s>",
        "special_separator": "[INST]",
        "inference_templates": [
            ministral3_base.replace("__RULE__", repr(shared_prompt)),
            ministral3_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "GLM_4": {
        "bos": "[gMASK]<sop>",
        "eos": "<|endoftext|>",
        "special_separator": "<|system|>",
        "inference_templates": [
            glm4_base.replace("__RULE__", repr(shared_prompt)),
            glm4_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "GPT_OSS": {
        "bos": "<|start|>",
        "eos": "<|end|>",
        "special_separator": "<|start|>",
        "inference_templates": [
            gpt_oss_base.replace("__RULE__", repr(shared_prompt)),
            gpt_oss_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "Spark_X2_5": {
        "bos": "<｜start▁of▁sentence｜>",
        "eos": "<｜end▁of▁sentence｜>",
        "special_separator": "<｜start▁of▁sentence｜>",
        "inference_templates": [
            spark_x2_5_base.replace("__RULE__", repr(shared_prompt)),
            spark_x2_5_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "Ling": {
        "bos": "<role>",
        "eos": "<|role_end|>",
        "special_separator": "<role>",
        "inference_templates": [
            ling_base.replace("__RULE__", repr(shared_prompt)),
            ling_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    },
    "Nemotron_Nano_v2": {
        "bos": "<SPECIAL_10>",
        "eos": "<SPECIAL_12>",
        "special_separator": "<SPECIAL_11>",
        "inference_templates": [
            nemotron_base.replace("__RULE__", repr(shared_prompt)),
            nemotron_base.replace("__RULE__", repr(shared_prompt_reasoning))
        ]
    }
}