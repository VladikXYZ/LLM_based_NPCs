import os
import sys
import json
import platform
import questionary
from llama_cpp import Llama

import utils
import npc_runtime
from chat_templates import MINI_REASONING_RULE
from utils import get_devices, get_models, MyException

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
GREY = "\033[90m"
RESET = "\033[0m"

CONTEXT_SIZE = 4096
MAX_TOKENS = 1024  # Increased for normal chatting
CUSTOM_JINJA = True
SYSTEM_PROMPT = "You are a helpful, smart, and concise AI assistant."


class InteractiveChat:
    def __init__(self):
        self.devices = get_devices()
        self.models = get_models()

        if not self.models:
            sys.exit(f"{RED}No models found in the models directory!{RESET}")

        # 1. Select Device
        device_choices = [f"{i} | {d['type']:<8} | {d['name']}" for i, d in enumerate(self.devices)]
        dev_choice = questionary.select("Select device:", choices=device_choices, qmark="🎮").ask()
        if not dev_choice: sys.exit("Exiting...")
        dev_idx = int(dev_choice.split("|")[0])
        self.device = self.devices[dev_idx]

        # 2. Select Model
        # print(self.models)
        model_choices = [f"{i} | {m['name']}" for i, m in enumerate(self.models)]
        mod_choice = questionary.select("Select model:", choices=model_choices, qmark="🧠").ask()
        if not mod_choice: sys.exit("Exiting...")
        mod_idx = int(mod_choice.split("|")[0])
        self.model = self.models[mod_idx]

        # 3. Select mini reasoning (plan <speech> dialogue); '/mini' toggles it during the chat
        self.mini = questionary.confirm("Mini reasoning?", default=False, qmark="💭").ask()
        if self.mini is None: sys.exit("Exiting...")

        # 4. Apply Hardware Settings
        print(f"\n⚡ Booting {self.model['name']} on {self.device['name']}...")
        self.gpu_layers = -1 if self.device["type"] == "Vulkan" else 0
        os.environ["GGML_VK_VISIBLE_DEVICES"] = str(self.device["id"] * (self.device["type"] == "Vulkan"))

        self._start_chat()

    def _system_message(self):
        # the custom templates add the rule themselves; the model's own template does not
        templated = CUSTOM_JINJA and self.model["family"]
        content = SYSTEM_PROMPT + (" " + MINI_REASONING_RULE if self.mini and not templated else "")
        return {"role": "system", "content": content}

    def _start_chat(self):
        llm_kwargs = {
            "model_path": self.model["path"],
            "n_gpu_layers": self.gpu_layers,
            "n_ctx": CONTEXT_SIZE,
            "verbose": False,
            "temperature": 0.7  # Better for generic chatting than 0
        }

        chat_history = [self._system_message()]
        warmup = chat_history + [{"role": "user", "content": "Hello"}]

        # Load using your utils function
        try:
            llm = utils.load_llm(self.model, llm_kwargs, warmup, custom_jinja=CUSTOM_JINJA, reason=self.mini, log=True)
            if not llm:
                sys.exit(f"\n{RED}Failed to load the model.{RESET}")
        except Exception as e:
            sys.exit(f"\n{RED}Error loading model: {e}{RESET}")

        print(f"\n{GREEN}========================================={RESET}")
        print(f"{GREEN} Chat Session Started! Type '/exit' to quit{RESET}")
        print(f"{GREEN} '/mini' toggles mini reasoning (now {'on' if self.mini else 'off'}){RESET}")
        print(f"{GREEN}========================================={RESET}")

        while True:
            try:
                # Get user input
                user_input = input(f"\n{GREEN}You:{RESET} ")

                # Check for exit commands
                if user_input.strip().lower() in ['/exit', '/quit']:
                    print("Ending session...")
                    break
                if user_input.strip().lower() == '/mini':
                    self.mini = not self.mini
                    utils.set_reasoning(llm, self.model, CUSTOM_JINJA, self.mini)
                    # old replies in the other format would be copied by the model, so the chat starts again
                    chat_history = [self._system_message()]
                    print(f"Mini reasoning {'on' if self.mini else 'off'}, conversation restarted")
                    continue
                if not user_input.strip():
                    continue

                # Add to history
                chat_history.append({"role": "user", "content": user_input})

                # Stream the generation; in mini mode the raw stream holds the plan as well
                print(f"{GREY}Raw:{RESET} " if self.mini else f"{BLUE}Assistant:{RESET} ", end="", flush=True)
                result = npc_runtime.generate(llm, chat_history, self.mini, MAX_TOKENS,
                                              on_text=lambda text: print(text, end="", flush=True))
                print()  # Newline after generation finishes

                if self.mini:
                    if result.format_ok:
                        print(f"{BLUE}NPC:{RESET} {result.dialogue}")
                        print(f"{GREY}first output {result.ttft:.2f} s | dialogue {result.dialogue_ttft:.2f} s{RESET}")
                    else:
                        print(f"{RED}Format error: expected 'plan <speech> dialogue'{RESET}")

                # The raw response goes to history, so the next prompt matches the KV cache
                chat_history.append({"role": "assistant", "content": result.raw})

            except KeyboardInterrupt:
                # Allows you to press Ctrl+C to cleanly exit the chat
                print("\nExiting chat...")
                break
            except Exception as e:
                print(f"\n{RED}Inference Error: {e}{RESET}")
                print("\nExiting chat...")
                break

        if hasattr(llm, 'close'):
            llm.close()
        del llm


if __name__ == '__main__':
    InteractiveChat()