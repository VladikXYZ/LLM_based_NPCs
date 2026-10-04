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

    "ling": {
        "bos": "",
        "eos": "<|role_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<role>SYSTEM</role>' + shared_prompt + '<|role_end|>' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<role>ASSISTANT</role>\n<think>\n\n</think>\n' + message.content + '<|role_end|>' -}}
    {%- else -%}
        {{- '<role>HUMAN</role>' + message.content + '<|role_end|>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<role>ASSISTANT</role>\n<think>\n\n</think>\n' -}}
{%- endif -%}"""
    },

    "llama": {
        "bos": "<|begin_of_text|>",
        "eos": "<|eot_id|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '<|start_header_id|>system<|end_header_id|>\n\n' + shared_prompt + '<|eot_id|>' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<|start_header_id|>assistant<|end_header_id|>\n\n<think>\n\n</think>\n\n' + message.content + '<|eot_id|>' -}}
    {%- else -%}
        {{- '<|start_header_id|>' + message.role + '<|end_header_id|>\n\n' + message.content + '<|eot_id|>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<|start_header_id|>assistant<|end_header_id|>\n\n<think>\n\n</think>\n\n' -}}
{%- endif -%}"""
    },

    "mistral": {
        "bos": "<s>",
        "eos": "</s>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- bos_token if bos_token is defined else '' -}}
{{- '[SYSTEM_PROMPT]' + shared_prompt + '[/SYSTEM_PROMPT]' -}}
{%- for message in messages -%}
    {%- if message.role == 'assistant' -%}
        {{- '<think>\n\n</think>\n\n' + message.content + (eos_token if eos_token is defined else '</s>') -}}
    {%- else -%}
        {{- '[INST]' + message.content + '[/INST]' -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '<think>\n\n</think>\n\n' -}}
{%- endif -%}"""
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

    "gemma": {
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
        {{- '\n<SPECIAL_11>Assistant\n<think>\n\n</think>\n' + message.content + '\n<SPECIAL_12>' -}}
    {%- else -%}
        {{- '\n<SPECIAL_11>User\n' + message.content -}}
    {%- endif -%}
{%- endfor -%}
{%- if add_generation_prompt -%}
{{- '\n<SPECIAL_11>Assistant\n<think>\n\n</think>\n' -}}
{%- endif -%}"""
    }
}