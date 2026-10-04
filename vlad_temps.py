TEMPLATES = {
    "chatml": {
        "bos": "",
        "eos": "<|im_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' + message.content + '<|im_end|>\n' -}}
    {%- else -%}
        {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' -}}
{%- endif -%}"""
    },

    # granite 4.2, Nemotron 3.5 / Nemotron3 Nano: their own templates write the empty think block without newlines
    "chatml_inline": {
        "bos": "",
        "eos": "<|im_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|im_start|>assistant\n<think></think>' + message.content + '<|im_end|>\n' -}}
    {%- else -%}
        {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|im_start|>assistant\n<think></think>' -}}
{%- endif -%}"""
    },

    # LFM2, LFM2.5 without reasoning: no think block (with one the small models answer nothing)
    "lfm": {
        "bos": "<|startoftext|>",
        "eos": "<|im_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
{%- for message in messages -%}
    {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|im_start|>assistant\n' -}}
{%- endif -%}"""
    },

    # LFM2.5 with reasoning: LFM writes its think block without newlines
    "lfm_think": {
        "bos": "<|startoftext|>",
        "eos": "<|im_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|im_start|>assistant\n<think></think>' + message.content + '<|im_end|>\n' -}}
    {%- else -%}
        {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|im_start|>assistant\n<think></think>' -}}
{%- endif -%}"""
    },

    "chatml_bos": {
        "bos": "<s>",
        "eos": "<|im_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' + message.content + '<|im_end|>\n' -}}
    {%- else -%}
        {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' -}}
{%- endif -%}"""
    },

    "glm": {
        "bos": "[gMASK]<sop>",
        "eos": "<|user|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '[gMASK]<sop><|system|>\n' + shared_prompt -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '\n<|assistant|>\n<think>\n\n</think>\n' + message.content -}}
    {%- else -%}
        {{- '\n<|' + message.role + '|>\n' + message.content -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '\n<|assistant|>\n<think>\n\n</think>\n' -}}
{%- endif -%}"""
    },

    # GLM 4.6V: no newline before a role tag, "/nothink" after every user message, think block without newlines
    "glm_v": {
        "bos": "[gMASK]<sop>",
        "eos": "<|user|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '[gMASK]<sop><|system|>\n' + shared_prompt -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|assistant|>\n<think></think>\n' + message.content -}}
    {%- elif message.role == 'user' -%}
        {{- '<|user|>\n' + message.content + '/nothink' -}}
    {%- else -%}
        {{- '<|' + message.role + '|>\n' + message.content -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|assistant|>\n<think></think>\n' -}}
{%- endif -%}"""
    },

    # Ling: reasoning is switched off in the system block, the reply follows the empty think block directly
    "ling": {
        "bos": "",
        "eos": "<|role_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<role>SYSTEM</role>' + shared_prompt + '\ndetailed thinking off<|role_end|>' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<role>ASSISTANT</role>\n<think></think>' + message.content + '<|role_end|>' -}}
    {%- else -%}
        {{- '<role>HUMAN</role>' + message.content + '<|role_end|>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<role>ASSISTANT</role>\n<think></think>' -}}
{%- endif -%}"""
    },

    # Llama has no think tokens: a think block is plain text to it
    "llama": {
        "bos": "<|begin_of_text|>",
        "eos": "<|eot_id|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '<|start_header_id|>system<|end_header_id|>\n\n' + shared_prompt + '<|eot_id|>' -}}
{%- for message in messages -%}
    {{- '<|start_header_id|>' + message.role + '<|end_header_id|>\n\n' + message.content + '<|eot_id|>' -}}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
{%- endif -%}"""
    },

    # Ministral has no think tokens: the reply follows [/INST] directly
    "mistral": {
        "bos": "<s>",
        "eos": "</s>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '[SYSTEM_PROMPT]' + shared_prompt + '[/SYSTEM_PROMPT]' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- message.content + (eos_token if eos_token is defined else '</s>') -}}
    {%- else -%}
        {{- '[INST]' + message.content + '[/INST]' -}}
    {%- endif -%}
{%- endfor -%}"""
    },

    "spark": {
        "bos": "",
        "eos": "<｜end▁of▁sentence｜>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<｜start▁of▁sentence｜><|System|>\n' + shared_prompt + '<｜end▁of▁sentence｜>' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<｜start▁of▁sentence｜><|Bot|><think>\n\n</think>\n\n' + message.content + '<｜end▁of▁sentence｜>' -}}
    {%- else -%}
        {{- '<｜start▁of▁sentence｜><|User|>' + message.content + '<｜end▁of▁sentence｜>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<｜start▁of▁sentence｜><|Bot|><think>\n\n</think>\n\n' -}}
{%- endif -%}"""
    },

    # gemma 4 E2B, E4B: no thought channel (with an empty one they write their reasoning into the reply)
    "gemma": {
        "bos": "<bos>",
        "eos": "<turn|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '<|turn>system\n' + shared_prompt + '<turn|>\n' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|turn>model\n' + message.content + '<turn|>\n' -}}
    {%- else -%}
        {{- '<|turn>user\n' + message.content + '<turn|>\n' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|turn>model\n' -}}
{%- endif -%}"""
    },

    # gemma 4 12B, 26B: empty thought channel (without it they write one themselves)
    "gemma_think": {
        "bos": "<bos>",
        "eos": "<turn|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '<|turn>system\n' + shared_prompt + '<turn|>\n' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|turn>model\n<|channel>thought\n\n<channel|>' + message.content + '<turn|>\n' -}}
    {%- else -%}
        {{- '<|turn>user\n' + message.content + '<turn|>\n' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|turn>model\n<|channel>thought\n\n<channel|>' -}}
{%- endif -%}"""
    },

    "gpt": {
        "bos": "",
        "eos": "<|end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<|start|>system<|message|>' + shared_prompt + '<|end|>' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|start|>assistant<|channel|>analysis<|message|>\n\n<|end|><|start|>assistant<|channel|>final<|message|>' + message.content + '<|end|>' -}}
    {%- else -%}
        {{- '<|start|>' + message.role + '<|message|>' + message.content + '<|end|>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|start|>assistant<|channel|>analysis<|message|>\n\n<|end|><|start|>assistant<|channel|>final<|message|>' -}}
{%- endif -%}"""
    },

    "nemotron": {
        "bos": "",
        "eos": "<SPECIAL_12>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<SPECIAL_10>System\n' + shared_prompt -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '\n<SPECIAL_11>Assistant\n<think></think>' + message.content + '\n<SPECIAL_12>' -}}
    {%- else -%}
        {{- '\n<SPECIAL_11>User\n' + message.content -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '\n<SPECIAL_11>Assistant\n<think></think>' -}}
{%- endif -%}"""
    }
}