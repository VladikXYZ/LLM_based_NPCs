import subprocess
import os
import json
import sys
import time
from tabnanny import verbose

import pandas
import platform
import questionary
import llama_cpp
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Jinja2ChatFormatter
from tqdm import tqdm

import utils
import vlad_temps
from utils import get_devices, get_models, MyException

# The rules go into the templates inside double quotes, so they must not contain any.
SHARED_RPG_RULE = "You are an NPC in a fantasy RPG. Reply with spoken dialogue only: no stage directions, actions, asterisks or quotation marks. Answer the player's exact question in at most 2 short sentences and volunteer nothing else. Use only facts from your knowledge base. Never invent names, places, people, items or events; if your knowledge base does not cover something, say in character that you do not know."

# Added after the shared rule: [no reasoning, mini reasoning], picked by REASON.
REASONING_RULE = [
    "DO NOT THINK. Reply with the dialogue immediately.",
    "OUTPUT FORMAT, mandatory in every reply: first a brief response plan (at most 2 sentences), then exactly one | separator, then the spoken dialogue. Example: The player wants directions, I will point the way. | The inn is past the well. The plan is not spoken: the dialogue rules apply only to the text after |.",
]

# MODEL_DIR = 'models/'
# DEVICES_FILE = "devices.json"
PC_NAME = platform.node()
LOG_DIR = f'benchmarks/{PC_NAME}/'
LOG_DIR = ""
# os.makedirs(LOG_DIR, exist_ok=True)
with open("data/shorts.json", "r") as f: SHORTS = json.load(f)[:4]
with open("data/longs.json", "r") as f: LONGS = json.load(f)[:4]
with open("data/data_3npcs.json") as file: NPC = json.load(file)[2]
CUSTOM_JINJA = True
REASON = False
if CUSTOM_JINJA:
    CHAT_HISTORY = []#[{"role": "system", "content": NPC["role"]}]
    WARMUP = []#CHAT_HISTORY[:]
else:
    CHAT_HISTORY = [{"role": "system", "content": NPC["role"] + NPC["shared_system_prompt"]}]
    WARMUP = CHAT_HISTORY[:] + [{"role": "user", "content": "warmup"}]

MESSAGES = [("long", LONGS), ("short", SHORTS)]
NUM_MESS = len(SHORTS+LONGS)
CONTEXT_SIZE = 4096
MAX_TOKENS = 64
TIMEOUT = (NUM_MESS * (0.9 + (MAX_TOKENS / 5.5))).__ceil__()
HEADER = ["MODEL", "TTFT", "T/s", "USER TOKENS", "NPC TOKENS", "TOTAL TIME", "ALL TOKENS", "PROMPT", "RESPONSE"]
ERROR_ROW = [-1 for _ in range(len(HEADER)-2)]


RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


class Benchmarker:
    def __init__(self, dev=None):
        self.models = get_models()
        self.devices = get_devices()
        self.formatter = None

        if dev is None:
            device_choices = [f"{i} | {d['type']:<8} | {d['name']}" for i, d in enumerate(self.devices)]
            dev_choice = questionary.select("Select device:", choices=device_choices, qmark="🎮").ask()
            if not dev_choice: sys.exit("Exiting...")
            dev_idx = int(dev_choice.split("|")[0])
            self.device = self.devices[dev_idx]
        else:
            if 0 <= dev < len(self.devices):self.device = self.devices[dev]
            else: sys.exit(f"Invalid device value:{dev}")

        print(f"\n⚡ Fast Start: Running Benchmark on {self.device['name']}...")
        self.gpu_layers = -1 if self.device["type"] == "Vulkan" else 0
        os.environ["GGML_VK_VISIBLE_DEVICES"] = str(self.device["id"] * (self.device["type"] == "Vulkan"))
        self._run_benchmark()

    def _cache(self, llm):
        self.formatter.add_generation_prompt = False
        warmup_prompt = self.formatter(messages=WARMUP).prompt
        warmup_tokens = llm.tokenize(warmup_prompt.encode("utf-8"), add_bos=False, special=True)
        llm.reset()
        llm.eval(warmup_tokens)
        llama_cpp.llama_synchronize(llm._ctx.ctx)
        self.formatter.add_generation_prompt = True
        return len(warmup_tokens)

    def _run_benchmark(self):
        dev_name = self.device["type"] + "_" + "_".join(self.device["name"].split())

        log = []
        num_models = len(self.models)
        test_start = time.perf_counter()
        chat_history = CHAT_HISTORY[:]
        print(f"{"CUSTOM JINJA" if CUSTOM_JINJA else "DEFAULT JINJA"} | {"MINI-REASONING" if REASON else "ONESHOT"} | DEVICE:{dev_name} | TIMEOUT:{TIMEOUT} | {num_models} MODELS")


        for i, model in enumerate(self.models):
            family = model["family"]
            model_log = []
            llm = None
            llm_kwargs = {"model_path": model["path"], "n_gpu_layers": self.gpu_layers,
                          "n_ctx": CONTEXT_SIZE, "verbose": False, "seed": 42}
            try:
                print(f"Loading {i+1}/{num_models}. {model["name"]} | ", end="", flush=True)
                with utils.Silencer():
                    try:
                        llm = Llama(**llm_kwargs)
                        print(f"Loaded! | ", end="", flush=True)
                        try:
                            templating = vlad_temps.TEMPLATES[family]
                            if CUSTOM_JINJA:
                                rule = f"{SHARED_RPG_RULE} {NPC["role"]} {REASONING_RULE[REASON]}"
                                template = templating["template"].replace("__RULE__", f"\"{rule}\"")
                                # print(template)
                                formatter = Jinja2ChatFormatter(template=template,
                                                                        eos_token=templating["eos"],
                                                                        bos_token=templating["bos"])
                                llm.chat_handler = formatter.to_chat_handler()
                                self.formatter = formatter
                            else:
                                formatter = Jinja2ChatFormatter(template=llm.metadata.get("tokenizer.chat_template"),
                                                                eos_token=templating["eos"],
                                                                bos_token=templating["bos"])
                                self.formatter = formatter
                            llm.create_chat_completion(WARMUP, max_tokens=4)
                            # self._cache(llm)
                            # self.formatter.add_generation_prompt = False
                            # print("KV Cache Primed!!", flush=True)
                            print("Warmuped!!", flush=True)
                            # print

                        except Exception as e: raise MyException("Warmup error", str(e))
                    except Exception as e:
                        if type(e) != MyException: raise MyException("Loading error", str(e))

                if not llm: raise MyException("Something went wron", "xdd")
                model_start = time.perf_counter()
                timeout = TIMEOUT

                for name, mess in MESSAGES:
                    prev_n = self._cache(llm)
                    for user_input in tqdm(mess, desc=f"Testing {model["name"]} on {name} queries", unit="query"):
                        chat_history.append({"role": "user", "content": user_input})
                        # print(self.formatter(messages=chat_history).prompt)
                        ttft = TIMEOUT*2
                        start_time = time.perf_counter()
                        assistant_response = []

                        stream = llm.create_chat_completion(messages=chat_history, stream=True, max_tokens=MAX_TOKENS)
                        for chunk in stream:
                            current = time.perf_counter()
                            if current - model_start <= TIMEOUT:
                                delta = chunk['choices'][0]["delta"]
                                if 'content' in delta:
                                    ttft = min(current-start_time, ttft)
                                    assistant_response.append(delta['content'])
                            else: raise MyException("Timeout!", f"Ran out of time ({TIMEOUT} s)")
                        string_response = "".join(assistant_response)
                        total_time = time.perf_counter() - start_time
                        gen_time = total_time - ttft
                        t_out = len(assistant_response)
                        tps = (t_out - 1) / gen_time if gen_time > 0 else -1
                        all_tokens = llm.n_tokens
                        t_in = len(llm.tokenize(user_input.encode("utf-8")))

                        # the history keeps the raw reply so that it matches the KV cache, the CSV gets it trimmed
                        chat_history.append({"role": "assistant", "content": string_response})
                        # query = user_input[:].replace('\n', '|')
                        # response = assistant_response[:].replace('\n', '|')
                        model_log.append([model["name"], ttft, tps, t_in, t_out, total_time, all_tokens, user_input, string_response.strip()])
                        prev_n = all_tokens
                    chat_history = CHAT_HISTORY[:]
                print(f"{GREEN}FINISHED!!!{RESET}")

            except Exception as e:
                # print(MyException)
                if type(e) != MyException: e = MyException("Inference error", str(e))
                print(f"{RED}{e.error_type}{RESET}")
                model_log.append([model["name"]] + ERROR_ROW +[str(e)])
                done = len(model_log)
                for _ in range(NUM_MESS - done): model_log.append([model["name"]] + ERROR_ROW + [-1])
            finally:
                if 'stream' in locals(): del stream
                if hasattr(llm, 'close'): llm.close()
                del llm
                log.extend(model_log)

        print(f"It all took: {time.perf_counter() - test_start}")

        xd = pandas.DataFrame(log, columns=HEADER)
        xd = xd.round(3)
        file_path = f"{LOG_DIR}{dev_name}.csv"
        print(f"Saved to {file_path}")
        xd.to_csv(file_path, index=False, float_format="%.3f")



if __name__ == '__main__':
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
        if num == -1:
            devices = get_devices()
            start = time.time()
            for j in range(len(devices)):
                prev = time.time()
                subprocess.run([sys.executable, "bench.py", str(j)])
                print(f"This took {time.time() - prev} seconds")
            print(f"All tests took {time.time() - start} seconds")
        else: Benchmarker(num)
    else: Benchmarker()
