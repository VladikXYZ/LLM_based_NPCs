#!/bin/bash
#PBS -N setup_gpu_env
#PBS -l select=1:ncpus=8:mem=32gb:scratch_local=40gb
#PBS -l walltime=03:00:00
#PBS -j oe
# Creates .conda-gpu: Python, CUDA 12.9 and compilers from conda-forge, and llama-cpp-python built with CUDA.
# The CUDA modules of MetaCentrum (up to 12.6) cannot compile against the C library of Debian 13, CUDA 12.9 can.
# Run from the repo root: qsub metacentrum/setup_gpu_env.sh
set -e
cd "$PBS_O_WORKDIR"
ENV="$PWD/.conda-gpu"
export TMPDIR="$SCRATCHDIR" CONDA_PKGS_DIRS="$SCRATCHDIR/pkgs"
source /etc/profile.d/30_meta_modules.sh
module load mambaforge/22.9.0
mamba create -y -q -p "$ENV" -c conda-forge python=3.13 pip cmake ninja cxx-compiler \
    cuda-version=12.9 cuda-nvcc cuda-cudart-dev libcublas-dev
eval "$(conda shell.bash hook)"
conda activate "$ENV"
# GPUs with at least 40 GB on MetaCentrum are compute capability 8.0 to 9.0 (newer ones run the 9.0 code)
export CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=80;86;89;90 -GNinja" CMAKE_BUILD_PARALLEL_LEVEL=8
pip install --no-cache-dir "llama-cpp-python==0.3.36"
pip install --no-cache-dir -r requirements.txt "huggingface_hub[hf_xet]"
python -c "import llama_cpp; print('llama-cpp-python', llama_cpp.__version__, '| GPU offload:', llama_cpp.llama_supports_gpu_offload())"
