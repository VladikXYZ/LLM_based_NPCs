# TEMPLATES = {
#     "chatml": {
#         "bos": "",
#         "eos": "<|im_end|>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' + message.content + '<|im_end|>\n' -}}
#     {%- else -%}
#         {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' -}}
# {%- endif -%}
# """
#     },
#
#     "chatml_nr": {
#         "bos": "",
#         "eos": "<|im_end|>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
# {%- for message in messages -%}
#     {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|im_start|>assistant\n' -}}
# {%- endif -%}
# """
#     },
#
#     "llama": {
#         "bos": "<|begin_of_text|>",
#         "eos": "<|eot_id|>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<|start_header_id|>system<|end_header_id|>\n\n' + shared_prompt + '<|eot_id|>' -}}
# {%- for message in messages -%}
#     {{- '<|start_header_id|>' + message.role + '<|end_header_id|>\n\n' + message.content + '<|eot_id|>' -}}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
# {%- endif -%}
# """
#     },
#
#     "gemma": {
#         "bos": "<bos>",
#         "eos": "<turn|>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<|turn>system\n' + shared_prompt + '<turn|>\n' -}}
# {%- for message in messages -%}
#     {%- set role = 'model' if message.role == 'assistant' else message.role -%}
#     {{- '<|turn>' + role + '\n' + message.content + '<turn|>\n' -}}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|turn>model\n<|channel>thought\n<channel|>' -}}
# {%- endif -%}
# """
#     },
#
#     "mistral": {
#         "bos": "<s>",
#         "eos": "</s>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '[SYSTEM_PROMPT]' + shared_prompt + '[/SYSTEM_PROMPT]' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'user' -%}
#         {{- '[INST]' + message.content + '[/INST]' -}}
#     {%- elif message.role == 'assistant' -%}
#         {{- message.content + '</s>' -}}
#     {%- endif -%}
# {%- endfor -%}
# """
#     },
#
#     "glm": {
#         "bos": "[gMASK]<sop>",
#         "eos": "<|user|>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# [gMASK]<sop><|system|>
# {{- shared_prompt -}}
# {%- for message in messages -%}
#     {%- if message.role == 'user' -%}
#         {{- '\n<|user|>\n' + message.content -}}
#     {%- elif message.role == 'assistant' -%}
#         {{- '\n<|assistant|>\n<think></think>' + message.content -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '\n<|assistant|>\n<think></think>' -}}
# {%- endif -%}
# """
#     },
#
#     "ling": {
#         "bos": "",
#         "eos": "<|role_end|>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<role>SYSTEM</role>' + shared_prompt + '\ndetailed thinking off<|role_end|>' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'user' -%}
#         {{- '<role>HUMAN</role>' + message.content + '<|role_end|>' -}}
#     {%- elif message.role == 'assistant' -%}
#         {{- '<role>ASSISTANT</role>\n<think></think>' + message.content + '<|role_end|>' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<role>ASSISTANT</role>\n<think></think>' -}}
# {%- endif -%}
# """
#     },
#
#     "spark": {
#         "bos": "",
#         "eos": "<｜end▁of▁sentence｜>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<｜start▁of▁sentence｜><|System|>\n' + shared_prompt + '<｜end▁of▁sentence｜>' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'user' -%}
#         {{- '<｜start▁of▁sentence｜><|User|>' + message.content + '<｜end▁of▁sentence｜>' -}}
#     {%- elif message.role == 'assistant' -%}
#         {{- '<｜start▁of▁sentence｜><|Bot|><think></think>' + message.content + '<｜end▁of▁sentence｜>' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<｜start▁of▁sentence｜><|Bot|><think></think>' -}}
# {%- endif -%}
# """
#     },
#
#     "gpt": {
#         "bos": "",
#         "eos": "<|end|>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<|start|>system<|message|>' + shared_prompt + '<|end|>' -}}
# {%- for message in messages -%}
#     {{- '<|start|>' + message.role + '<|message|>' + message.content + '<|end|>' -}}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|start|>assistant<|channel|>final<|message|>' -}}
# {%- endif -%}
# """
#     },
#
#     "nemotron": {
#         "bos": "",
#         "eos": "<SPECIAL_12>",
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<SPECIAL_10>System\n' + shared_prompt -}}
# {%- for message in messages -%}
#     {%- if message.role == 'user' -%}
#         {{- '\n<SPECIAL_11>User\n' + message.content -}}
#     {%- elif message.role == 'assistant' -%}
#         {{- '\n<SPECIAL_11>Assistant\n<think></think>' + message.content + '\n<SPECIAL_12>' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '\n<SPECIAL_11>Assistant\n<think></think>' -}}
# {%- endif -%}
# """
#     }
# }
#
# TEMPLATES = {
#     # Models: Bonsai, Nemotron, Qwen, Granite, Maple[cite: 1]
#     "chatml": {
#         "bos": "", #[cite: 1]
#         "eos": "<|im_end|>", #[cite: 1]
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' + message.content + '<|im_end|>\n' -}}
#     {%- else -%}
#         {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: LFM2, LFM2.5, MiniCPM5[cite: 1]
#     "chatml_bos": {
#         "bos": "{{- bos_token -}}", #[cite: 1]
#         "eos": "<|im_end|>", #[cite: 1]
#         "template": """{{- bos_token -}}
# {%- set shared_prompt = __RULE__ -%}
# {{- '<|im_start|>system\n' + shared_prompt + '<|im_end|>\n' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' + message.content + '<|im_end|>\n' -}}
#     {%- else -%}
#         {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|im_start|>assistant\n<think>\n\n</think>\n\n' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: GLM-4.6V, GLM-4.7[cite: 1]
#     "glm": {
#         "bos": "[gMASK]<sop>", #[cite: 1]
#         "eos": "", #[cite: 1]
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '[gMASK]<sop><|system|>\n' + shared_prompt -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<|assistant|>\n<think>\n\n</think>\n' + message.content -}}
#     {%- else -%}
#         {{- '<|' + message.role + '|>\n' + message.content -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|assistant|>\n<think>\n\n</think>\n' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: Ling-3.0-tiny[cite: 1]
#     "ling": {
#         "bos": "", #[cite: 1]
#         "eos": "<|role_end|>", #[cite: 1]
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<role>SYSTEM</role>' + shared_prompt + '<|role_end|>' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<role>ASSISTANT</role>\n<think>\n\n</think>' + message.content + '<|role_end|>' -}}
#     {%- else -%}
#         {{- '<role>HUMAN</role>' + message.content + '<|role_end|>' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<role>ASSISTANT</role>\n<think>\n\n</think>' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: Llama-3.1, Llama-3.2[cite: 1]
#     "llama": {
#         "bos": "{{- bos_token -}}", #[cite: 1]
#         "eos": "<|eot_id|>", #[cite: 1]
#         "template": """{{- bos_token -}}
# {%- set shared_prompt = __RULE__ -%}
# {{- '<|start_header_id|>system<|end_header_id|>\n\n' + shared_prompt + '<|eot_id|>' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<|start_header_id|>assistant<|end_header_id|>\n\n<think>\n\n</think>\n\n' + message.content + '<|eot_id|>' -}}
#     {%- else -%}
#         {{- '<|start_header_id|>' + message.role + '<|end_header_id|>\n\n' + message.content + '<|eot_id|>' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|start_header_id|>assistant<|end_header_id|>\n\n<think>\n\n</think>\n\n' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: Ministral-3[cite: 1]
#     "mistral": {
#         "bos": "{{- bos_token -}}", #[cite: 1]
#         "eos": "{{- eos_token -}}", #[cite: 1]
#         "template": """{{- bos_token -}}
# {%- set shared_prompt = __RULE__ -%}
# {{- '[SYSTEM_PROMPT]' + shared_prompt + '[/SYSTEM_PROMPT]' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<think>\n\n</think>\n\n' + message.content + eos_token -}}
#     {%- else -%}
#         {{- '[INST]' + message.content + '[/INST]' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<think>\n\n</think>\n\n' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: Spark-X2.5[cite: 1]
#     "spark": {
#         "bos": "", #[cite: 1]
#         "eos": "<｜end▁of▁sentence｜>", #[cite: 1]
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<｜start▁of▁sentence｜><|System|>\n' + shared_prompt + '<｜end▁of▁sentence｜>' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<｜start▁of▁sentence｜><|Bot|><think>\n\n</think>\n\n' + message.content + '<｜end▁of▁sentence｜>' -}}
#     {%- else -%}
#         {{- '<｜start▁of▁sentence｜><|User|>' + message.content + '<｜end▁of▁sentence｜>' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<｜start▁of▁sentence｜><|Bot|><think>\n\n</think>\n\n' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: gemma-4[cite: 1]
#     "gemma": {
#         "bos": "{{- bos_token -}}", #[cite: 1]
#         "eos": "<turn|>", #[cite: 1]
#         "template": """{{- bos_token -}}
# {%- set shared_prompt = __RULE__ -%}
# {{- '<|turn>system\n' + shared_prompt + '<turn|>\n' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<|turn>model\n<|channel>thought\n\n<channel|>' + message.content + '<turn|>\n' -}}
#     {%- else -%}
#         {{- '<|turn>user\n' + message.content + '<turn|>\n' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|turn>model\n<|channel>thought\n\n<channel|>' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: gpt-oss-20b[cite: 1]
#     "gpt": {
#         "bos": "", #[cite: 1]
#         "eos": "<|end|>", #[cite: 1]
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<|start|>system<|message|>' + shared_prompt + '<|end|>' -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<|start|>assistant<|channel|>analysis<|message|>\n\n<|end|><|start|>assistant<|channel|>final<|message|>' + message.content + '<|end|>' -}}
#     {%- else -%}
#         {{- '<|start|>' + message.role + '<|message|>' + message.content + '<|end|>' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<|start|>assistant<|channel|>analysis<|message|>\n\n<|end|><|start|>assistant<|channel|>final<|message|>' -}}
# {%- endif -%}""" #[cite: 1]
#     },
#
#     # Models: nvidia_NVIDIA-Nemotron-Nano-9B-v2[cite: 1]
#     "nemotron": {
#         "bos": "", #[cite: 1]
#         "eos": "<SPECIAL_12>", #[cite: 1]
#         "template": """{%- set shared_prompt = __RULE__ -%}
# {{- '<SPECIAL_10>System\n' + shared_prompt -}}
# {%- for message in messages -%}
#     {%- if message.role == 'assistant' -%}
#         {{- '<SPECIAL_11>Assistant\n<think>\n\n</think>\n' + message.content + '\n<SPECIAL_12>\n' -}}
#     {%- else -%}
#         {{- '<SPECIAL_11>User\n' + message.content + '\n' -}}
#     {%- endif -%}
# {%- endfor -%}
# {%- if not not_generate -%}
# {{- '<SPECIAL_11>Assistant\n<think>\n\n</think>\n' -}}
# {%- endif -%}""" #[cite: 1]
#     }
# }

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