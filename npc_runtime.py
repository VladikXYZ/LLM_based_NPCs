"""Mini reasoning: parsing of "plan <speech> dialogue" replies and streaming with timings."""
import re
import time
from dataclasses import dataclass

SEPARATOR = "<speech>"
# A native thinking block in front of the reply is not part of the mini reasoning format.
NATIVE_THINKING = re.compile(r"^\s*<think>.*?</think>", re.DOTALL)


def split_response(raw, mini=False):
    """Return (plan, dialogue, format_ok). A malformed reply never yields dialogue."""
    text = NATIVE_THINKING.sub("", raw, count=1)
    if "<think>" in text or "</think>" in text:
        return "", "", False
    if not mini:
        ok = bool(text.strip()) and SEPARATOR not in text
        return "", text.strip() if ok else "", ok
    if text.count(SEPARATOR) != 1:
        return "", "", False
    plan, dialogue = (part.strip() for part in text.split(SEPARATOR))
    # some models close the separator even though only the opening one is asked for
    if dialogue.endswith("</speech>"):
        dialogue = dialogue[:-len("</speech>")].rstrip()
    ok = bool(plan and dialogue) and "</speech>" not in plan and "</speech>" not in dialogue
    return plan, dialogue if ok else "", ok


@dataclass
class Generation:
    raw: str = ""
    plan: str = ""
    dialogue: str = ""
    format_ok: bool = False
    ttft: float = -1           # seconds to the first output
    dialogue_ttft: float = -1  # seconds to the first dialogue (after <speech> in mini mode), -1 if the format is wrong
    total_time: float = -1
    chunks: int = 0


def generate(llm, messages, mini=False, max_tokens=256, on_text=None):
    """Stream one reply. on_text gets every raw piece, the plan included."""
    result = Generation()
    start = time.perf_counter()
    for chunk in llm.create_chat_completion(messages=messages, stream=True, max_tokens=max_tokens):
        content = chunk["choices"][0]["delta"].get("content")
        if not content: continue
        elapsed = time.perf_counter() - start
        result.raw += content
        result.chunks += 1
        if result.ttft < 0 and result.raw.strip():
            result.ttft = elapsed
        if result.dialogue_ttft < 0 and split_response(result.raw, mini)[1]:
            result.dialogue_ttft = elapsed
        if on_text: on_text(content)
    result.total_time = time.perf_counter() - start
    result.plan, result.dialogue, result.format_ok = split_response(result.raw, mini)
    if not result.format_ok:
        result.dialogue_ttft = -1
    return result
