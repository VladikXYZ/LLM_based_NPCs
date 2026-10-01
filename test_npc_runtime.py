"""Checks of the mini reasoning runtime. Needs no model: run `python test_npc_runtime.py` (or pytest)."""
from npc_runtime import generate, split_response


class FakeLlm:
    def __init__(self, pieces):
        self.pieces = pieces

    def create_chat_completion(self, messages, stream, max_tokens):
        yield {"choices": [{"delta": {"role": "assistant"}}]}
        for piece in self.pieces:
            yield {"choices": [{"delta": {"content": piece}}]}


def test_split_mini():
    assert split_response("He wants a sword. <speech> Ten gold.", True) == ("He wants a sword.", "Ten gold.", True)
    assert split_response("plan<speech>hello</speech>", True) == ("plan", "hello", True)
    # a native thinking block in front is not part of the format
    assert split_response("<think>\n\n</think>\n\nplan <speech> hello", True) == ("plan", "hello", True)
    for bad in ("", "plan only", "<speech>hello", "plan<speech>", "p<speech>x<speech>y",
                "p<speech>x</speech>extra", "<think>never closed plan <speech> x", "p <speech> x </think>"):
        plan, dialogue, ok = split_response(bad, True)
        assert not ok and dialogue == "", bad


def test_split_off():
    assert split_response(" Ten gold. ") == ("", "Ten gold.", True)
    assert split_response("<think>hm</think>Ten gold.") == ("", "Ten gold.", True)
    for bad in ("", "   ", "plan <speech> hello", "<think>never closed"):
        assert split_response(bad) == ("", "", False), bad


def test_generate_mini():
    seen = []
    result = generate(FakeLlm([" ", "He wants", " a sword. <speech>", " ", "Ten", " gold."]), [], mini=True, on_text=seen.append)
    assert result.raw == "".join(seen) == " He wants a sword. <speech> Ten gold."
    assert (result.plan, result.dialogue, result.format_ok) == ("He wants a sword.", "Ten gold.", True)
    assert 0 <= result.ttft <= result.dialogue_ttft <= result.total_time
    assert result.chunks == 6


def test_generate_wrong_format():
    result = generate(FakeLlm(["Ten", " gold."]), [], mini=True)
    assert not result.format_ok and result.dialogue == "" and result.dialogue_ttft == -1
    assert result.ttft >= 0 and result.raw == "Ten gold."


def test_generate_off():
    result = generate(FakeLlm(["Ten", " gold."]), [])
    assert (result.plan, result.dialogue, result.format_ok) == ("", "Ten gold.", True)
    assert result.dialogue_ttft == result.ttft >= 0


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
