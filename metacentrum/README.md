# Running on MetaCentrum

All commands are run on a frontend (e.g. `tarkil.metacentrum.cz`) from the root of the repo. `qsub` needs a valid Kerberos ticket (`kinit`).

1. Models (about 240 GB): a Python environment with `huggingface_hub`, then the download job.
   ```bash
   python3 -m venv --without-pip .venv && curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
   .venv/bin/pip install -U "huggingface_hub[hf_xet]"
   qsub metacentrum/download_models.sh
   ```
2. GPU environment (once): CUDA 12.9 and llama-cpp-python built with CUDA, in `.conda-gpu`.
   ```bash
   qsub metacentrum/setup_gpu_env.sh
   ```
3. The jailbreak tests on one GPU: `qsub metacentrum/run_tester.sh`. The results are written to the repo root.
4. CUDA against Vulkan on the same GPU: build the Vulkan environment once, then the comparison job. It copies the
   repo and all models to the node's local disk, runs `tester.py` with CUDA and then with Vulkan, and writes the
   results, logs and timings (`summary.txt`) to `results/metacentrum/<job id>/`.
   ```bash
   qsub metacentrum/setup_vulkan_env.sh
   qsub metacentrum/compare_backends.sh
   ```

`qstat -u $USER` shows the jobs, the output of a job is in `<job name>.o<job id>` in the repo root.
