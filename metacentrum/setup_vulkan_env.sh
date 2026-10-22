#!/bin/bash
#PBS -N setup_vulkan_env
#PBS -l select=1:ncpus=8:mem=32gb:scratch_local=40gb
#PBS -l walltime=03:00:00
#PBS -j oe
# Creates .conda-vulkan: Python, the Vulkan loader, headers and shader compiler from conda-forge,
# and llama-cpp-python built with Vulkan (the same backend as on our own PCs).
# The NVIDIA Vulkan driver itself comes from the GPU node (see compare_backends.sh).
# Run from the repo root: qsub metacentrum/setup_vulkan_env.sh
set -e
cd "$PBS_O_WORKDIR"
ENV="$PWD/.conda-vulkan"
export TMPDIR="$SCRATCHDIR" CONDA_PKGS_DIRS="$SCRATCHDIR/pkgs"
source /etc/profile.d/30_meta_modules.sh
module load mambaforge/22.9.0
mamba create -y -q -p "$ENV" -c conda-forge python=3.13 pip cmake ninja cxx-compiler \
    vulkan-headers libvulkan-loader shaderc vulkan-tools
eval "$(conda shell.bash hook)"
conda activate "$ENV"
export VULKAN_SDK="$ENV"   # where CMake looks for the Vulkan headers, library and glslc
export CMAKE_ARGS="-DGGML_VULKAN=on -GNinja" CMAKE_BUILD_PARALLEL_LEVEL=8
pip install --no-cache-dir "llama-cpp-python==0.3.36"
pip install --no-cache-dir -r requirements.txt
ls "$ENV"/lib/python3.13/site-packages/llama_cpp/lib/libggml-vulkan.so && echo "llama-cpp-python built with Vulkan"
