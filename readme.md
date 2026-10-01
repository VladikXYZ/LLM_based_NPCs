# Cross-Platform LLM Setup

This repository contains the configuration and logic to run **llama-cpp-python** with hardware acceleration on all Vulkan supported devices.

## 🚀 Quick Start

### Prerequisites

*   **Python 3.12+**
    *   Ensure Python is installed and added to your system PATH.
*   **C++ compiler** (llama-cpp-python is built from source)
    *   Windows: [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the **Desktop development with C++** workload.
    *   Linux: `build-essential` (or your distro's equivalent).
*   **Vulkan SDK** (Tested on 1.4.341.1)
    *   [Download here](https://vulkan.lunarg.com/sdk/home) if not installed. Verify your installation with:
    ```bash
    vulkaninfo --summary
    ```
    * Vulkan SDK required components:
      * The Vulkan SDK Core
      * GLM Headers.
      * SDL libraries and headers.
      * Volk header, source, and library.
      * Vulkan Memory Allocator header.
      * Vulkan tools, header and spirv headers
*   **CMake** (Tested on 4.3.2)
    *   [Download here](https://cmake.org/download/) if missing. Verify with:
    ```bash
    cmake --version
    ```
    *   Visual Studio's bundled CMake also works (it is available inside the Developer Prompt below).

### 1. Create and activate a virtual environment

Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```
Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install llama-cpp-python with Vulkan

#### Windows 11
Open **"x64 Native Tools Command Prompt for VS 2022"** (so the compiler is on PATH), `cd` into the repo, activate the venv, then run in PowerShell:
```powershell
$env:CMAKE_ARGS="-DGGML_VULKAN=on -GNinja"; pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --no-binary llama-cpp-python
```
`-GNinja` makes the build use Ninja, which compiles in parallel on all CPU cores. Install it with `pip install ninja` if `ninja --version` fails.

> **Path-length error?** If pip fails with `No such file or directory` on a very long path
> (`vendor/llama.cpp/tools/ui/...`), either enable Windows long paths or use a short temp directory:
> ```powershell
> mkdir C:\t; $env:TMP="C:\t"; $env:TEMP="C:\t"
> ```
> then re-run the install command.

<!--
Otherwise add location of VulkanSDK:
```powershell
$env:CMAKE_ARGS="-DGGML_VULKAN=on -DVulkan_SDK='C:\VulkanSDK\1.4.341.1' -DVulkan_INCLUDE_DIR='C:\VulkanSDK\1.4.341.1\Include' -DVulkan_LIBRARY='C:\VulkanSDK\1.4.341.1\Lib\vulkan-1.lib'"; pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --no-binary llama-cpp-python
```
-->
---

#### 🐧 Linux (Ubuntu 24.04 and CachyOS)
Vulkan:
```bash
export CMAKE_ARGS="-DGGML_VULKAN=on"
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --no-binary llama-cpp-python
```
Vulkan, using ninja:
```bash
CMAKE_ARGS="-DGGML_VULKAN=on -GNinja" pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --no-binary llama-cpp-python
```
CUDA (NVIDIA only), using ninja:
```bash
CMAKE_ARGS="-DGGML_CUDA=on -GNinja" pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --no-binary llama-cpp-python
```

---

### 3. Install the remaining dependencies
```bash
pip install -r requirements.txt
```

### 4. Run

On first launch the scripts scan for devices (CPU and every Vulkan GPU) and cache them in `data/devices.json`. Delete that file to re-scan.

```bash
python chat.py     # interactive chat: pick a device and a model
python bench.py    # benchmark
```

Models are `.gguf` files in `models/` that are listed in `data/models.json` (matched by `path`). The Supra model (`Supra-Router-51M-Q1_0.gguf`) is included by default, so you can check that everything works by running `python bench.py 0` (device `0` from the device list). It is a tiny router model, so its output is not meaningful chat; it only verifies the install. Download other GGUF models into `models/` to use them.

### Mini reasoning

In mini reasoning mode the NPC is told to write a brief plan, then one `|` separator, then what it says:
`Brief response plan | Spoken dialogue`. The reply is split into a plan and a dialogue (`npc_runtime.py`),
the format is checked, and both the time to the first output and the time to the dialogue are measured.

* `python chat.py` asks whether to use it, and `/mini` switches it during the chat (the conversation restarts).
  The raw stream shows the plan, the NPC dialogue is printed separately.
* `python bench.py 0 --mini` benchmarks it. The `DIALOGUE TTFT` and `FORMAT OK` columns hold the result (`-1` and `0` for a wrong format).

`python test_templates.py` and `python test_npc_runtime.py` check the templates and the parsing without a model.

`python check_models.py 0` talks to every model in `models/` for a few turns in both modes and prints one table: BOS token, plain replies, replies that stop by themselves, KV cache reuse and the mini reasoning format. The columns are described at the top of the script.

> **Windows:** if output is piped/redirected and Python crashes with `UnicodeEncodeError`, set `PYTHONUTF8=1`.
