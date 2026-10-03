TEMPLATES_INFERENCE = {
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
{%- if not not_generate -%}
{{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' -}}
{%- endif -%}
"""
    },

    "chatml_nr": {
        "bos": "",
        "eos": "<|im_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
{%- for message in messages -%}
    {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
{%- endfor -%}
{%- if not not_generate -%}
{{- '<|im_start|>assistant\n' -}}
{%- endif -%}
"""
    },

    "llama": {
        "bos": "<|begin_of_text|>",
        "eos": "<|eot_id|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<|start_header_id|>system<|end_header_id|>\n\n' + shared_prompt + '<|eot_id|>' -}}
{%- for message in messages -%}
    {{- '<|start_header_id|>' + message.role + '<|end_header_id|>\n\n' + message.content + '<|eot_id|>' -}}
{%- endfor -%}
{%- if not not_generate -%}
{{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
{%- endif -%}
"""
    },

    "gemma": {
        "bos": "<bos>",
        "eos": "<turn|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<|turn>system\n' + shared_prompt + '<turn|>\n' -}}
{%- for message in messages -%}
    {%- set role = 'model' if message.role == 'assistant' else message.role -%}
    {{- '<|turn>' + role + '\n' + message.content + '<turn|>\n' -}}
{%- endfor -%}
{%- if not not_generate -%}
{{- '<|turn>model\n<|channel>thought\n<channel|>' -}}
{%- endif -%}
"""
    },

    "mistral": {
        "bos": "<s>",
        "eos": "</s>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '[SYSTEM_PROMPT]' + shared_prompt + '[/SYSTEM_PROMPT]' -}}
{%- for message in messages -%}
    {%- if message.role == 'user' -%}
        {{- '[INST]' + message.content + '[/INST]' -}}
    {%- elif message.role == 'assistant' -%}
        {{- message.content + '</s>' -}}
    {%- endif -%}
{%- endfor -%}
"""
    },

    "glm": {
        "bos": "[gMASK]<sop>",
        "eos": "<|user|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
[gMASK]<sop><|system|>
{{- shared_prompt -}}
{%- for message in messages -%}
    {%- if message.role == 'user' -%}
        {{- '\n<|user|>\n' + message.content -}}
    {%- elif message.role == 'assistant' -%}
        {{- '\n<|assistant|>\n<think></think>' + message.content -}}
    {%- endif -%}
{%- endfor -%}
{%- if not not_generate -%}
{{- '\n<|assistant|>\n<think></think>' -}}
{%- endif -%}
"""
    },

    "ling": {
        "bos": "",
        "eos": "<|role_end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<role>SYSTEM</role>' + shared_prompt + '\ndetailed thinking off<|role_end|>' -}}
{%- for message in messages -%}
    {%- if message.role == 'user' -%}
        {{- '<role>HUMAN</role>' + message.content + '<|role_end|>' -}}
    {%- elif message.role == 'assistant' -%}
        {{- '<role>ASSISTANT</role>\n<think></think>' + message.content + '<|role_end|>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if not not_generate -%}
{{- '<role>ASSISTANT</role>\n<think></think>' -}}
{%- endif -%}
"""
    },

    "spark": {
        "bos": "",
        "eos": "<｜end▁of▁sentence｜>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<｜start▁of▁sentence｜><|System|>\n' + shared_prompt + '<｜end▁of▁sentence｜>' -}}
{%- for message in messages -%}
    {%- if message.role == 'user' -%}
        {{- '<｜start▁of▁sentence｜><|User|>' + message.content + '<｜end▁of▁sentence｜>' -}}
    {%- elif message.role == 'assistant' -%}
        {{- '<｜start▁of▁sentence｜><|Bot|><think></think>' + message.content + '<｜end▁of▁sentence｜>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if not not_generate -%}
{{- '<｜start▁of▁sentence｜><|Bot|><think></think>' -}}
{%- endif -%}
"""
    },

    "gpt": {
        "bos": "",
        "eos": "<|end|>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<|start|>system<|message|>' + shared_prompt + '<|end|>' -}}
{%- for message in messages -%}
    {{- '<|start|>' + message.role + '<|message|>' + message.content + '<|end|>' -}}
{%- endfor -%}
{%- if not not_generate -%}
{{- '<|start|>assistant<|channel|>final<|message|>' -}}
{%- endif -%}
"""
    },

    "nemotron": {
        "bos": "",
        "eos": "<SPECIAL_12>",
        "template": """{%- set shared_prompt = __RULE__ -%}
{{- '<SPECIAL_10>System\n' + shared_prompt -}}
{%- for message in messages -%}
    {%- if message.role == 'user' -%}
        {{- '\n<SPECIAL_11>User\n' + message.content -}}
    {%- elif message.role == 'assistant' -%}
        {{- '\n<SPECIAL_11>Assistant\n<think></think>' + message.content + '\n<SPECIAL_12>' -}}
    {%- endif -%}
{%- endfor -%}
{%- if not not_generate -%}
{{- '\n<SPECIAL_11>Assistant\n<think></think>' -}}
{%- endif -%}
"""
    }
}