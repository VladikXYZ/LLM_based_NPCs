import json
import os
import subprocess
import sys
import re
import tempfile
import time
from contextlib import contextmanager
from math import inf

from llama_cpp import Llama
from llama_cpp.llama_chat_format import Jinja2ChatFormatter
from chat_templates import EOS_TOKENS, INFERENCE_TYPES, WARMUP_TYPES, TEMPLATES_INFERENCE

DEVICES_FILE = "data/devices.json"
MODELS_FILE = "data/models.json"
MODELS_DIRECTORY = "models"

class MyException(Exception):
    def __init__(self, error_type, message):
        super().__init__(message)
        self.message = message
        self.error_type = error_type

    def __str__(self):
        return f"<ERROR: {self.error_type.replace("\n", "")}> {self.message.replace("\n", "")}"

@contextmanager
def Silencer(suppress=True):
    if suppress:
        old_stderr = os.dup(sys.stderr.fileno())
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stderr.fileno())
        try: yield
        finally:
            os.dup2(old_stderr, sys.stderr.fileno())
            os.close(old_stderr)
            os.close(devnull)
    else: yield

@contextmanager
def Catcher():
    sys.stdout.flush()
    sys.stderr.flush()
    fd_out = sys.stdout.fileno()
    fd_err = sys.stderr.fileno()
    
    old_out = os.dup(fd_out)
    old_err = os.dup(fd_err)
    
    with tempfile.TemporaryFile() as tmp:
        os.dup2(tmp.fileno(), fd_out)
        os.dup2(tmp.fileno(), fd_err)

        logs = [""]
        try: yield logs
        finally:
            sys.stdout.flush()
            sys.stderr.flush()

            os.dup2(old_out, fd_out)
            os.dup2(old_err, fd_err)
            os.close(old_out)
            os.close(old_err)

            tmp.seek(0)
            logs[0] = tmp.read().decode('utf-8', errors='replace')


def _find_device():
    print("🔍 Scanning hardware... (this takes a second)")
    script = f"""
import sys
from llama_cpp import Llama
try:
   llm = Llama(model_path='models/Supra-Router-51M-Q1_0.gguf', n_gpu_layers=1, verbose=True)
except Exception:
   pass
    """
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, encoding='utf-8')
    devices = []
    for line in result.stderr.split('\n'):
        match = re.search(r"ggml_vulkan:\s+(\d+)\s+=\s+(.*?)\s+\|", line)
        if match:
            devices.append({"id": match.group(1), "name": match.group(2).strip(), "type": "Vulkan"})

    cpu_id = str(len(devices))
    devices.append({"id": cpu_id, "name": "CPU", "type": "CPU"})

    with open(DEVICES_FILE, "w") as f:
        json.dump(devices, f)
    return devices

def get_devices():
    try:
        with open(DEVICES_FILE, "r") as f:
            devices = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        devices = _find_device()
    return devices

def get_models():
    models = sorted([os.path.basename(x) for x in os.listdir(MODELS_DIRECTORY) if x.endswith(".gguf")],
                    key=os.path.basename)
    current = set([f"models/{x}" for x in models])
    with open(MODELS_FILE, "r") as f:
        models =  json.load(f)
    usable = []
    for model in models:
        if model["path"] in current: usable.append(model)
    return usable


with open("data/temps.json") as f:
    TEMPLATES = json.load(f)

def get_handlers(family: str, custom: bool, reason: bool):
    if not family or not custom: return None, None

    style = TEMPLATES[family]
    handler_inference = Jinja2ChatFormatter(template=style["template"][reason], eos_token=style["eos"],
                                            bos_token=style["bos"]).to_chat_handler()

    # if family == "chatml":
    #     handler_warmup = Jinja2ChatFormatter(
    #         template=warmup,
    #         eos_token=EOS_TOKENS[family],
    #         bos_token=""
    #     ).to_chat_handler()
    #
    #     return handler_inference, handler_warmup
    return handler_inference, None


def load_llm(model, llm_kwargs, warmup_inputs=[{"role":"user", "content":"warmup!"}], custom_jinja=False, reason = False, log = False):
    print(f"Loading {model["name"]} | ", end="", flush=True)

    infer, warmup = get_handlers(model["family"], custom_jinja, reason)
    if warmup:
        llm_kwargs["chat_handler"] = warmup
    elif infer:
        llm_kwargs["chat_handler"] = infer
    llm, err = None, None
    with Silencer():
        try:

            llm = Llama(**llm_kwargs, seed=42)
            print(f"Loaded! | ", end="", flush=True)

            try:
                llm.create_chat_completion(warmup_inputs, max_tokens=1)
                if warmup: llm.chat_handler = infer
                print("Warmuped!!", flush=True)
                return llm

            except Exception as e:
                if hasattr(llm, 'close'): llm.close()
                del llm
                err = f"Crashed during generation: {e}"
        except Exception as e:
            err = f"Crashed during loading: {e}"

    if err:
        if not log: raise Exception("Failed to load model.")
        llm_kwargs["verbose"] = True
        with Catcher() as c:
            try:
                llm = Llama(**llm_kwargs)
                llm.create_chat_completion(warmup_inputs, max_tokens=1)
            except:
                llm = None
        print("")
        raise MyException(err, c[0])



if __name__ == '__main__':
    pass
    models = sorted([os.path.basename(x) for x in os.listdir(MODELS_DIRECTORY) if x.endswith(".gguf")],key=os.path.basename)
    print(models)
    reals = set([f"models/{x}" for x in models])
    print(reals)
    models_dicts = []
    for model in models:
        name = model.lower().split(".")[:-1]
        name = "".join(name)
        print(name)
        if "gemma" in name: family = "gemma"
        elif "gpt" in name: family = "gptoss"
        elif "spark" in name: family = "spark"
        elif "llama" in name: family = "llama"
        elif "ministral" in name: family = "mistral"
        elif "glm" in name: family = "glm"
        elif any(k in name for k in ["qwen", "bonsai", "gpt", "nemotron", "ling", "spark", "granite", "minicpm", "maple"]):
            family = "chatml"
        elif any(k in name for k in ["lfm"]):
            family = "chatml_nr"
        else: family = None
        m_dict = {"name": name.replace("-", " "), "path": f"models/{model}", "family": family, "params": os.path.getsize(f"models/{model}")}
        models_dicts.append(m_dict)

    models_dicts = sorted(models_dicts, key=lambda x: x["params"], reverse=True)

    with open(MODELS_FILE, "w") as f:
        json.dump(models_dicts, f, indent=1)

    # with open("models/backup.json", "r") as f:
    #     models_dicts = json.load(f)
    # big_dict = {}
    # print(models_dicts)
    # for model in models_dicts:
    #     big_dict[model["path"].split("/")[-1]] = model
    # print(big_dict)
    # with open(MODELS_FILE, "w") as f:
    #     json.dump(models_dicts, f, indent=1)
    #     # print("skibidi")
