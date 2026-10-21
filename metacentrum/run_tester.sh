#!/bin/bash
#PBS -N npc_tester
#PBS -q gpu
#PBS -l select=1:ncpus=8:ngpus=1:gpu_mem=40gb:mem=64gb:scratch_local=10gb
#PBS -l walltime=24:00:00
#PBS -j oe
# Runs tester.py on one GPU with at least 40 GB (the biggest model takes 22 GB).
# Run from the repo root after setup_gpu_env.sh: qsub metacentrum/run_tester.sh
set -e
cd "$PBS_O_WORKDIR"
ENV="$PWD/.conda-gpu"
export PATH="$ENV/bin:$PATH" LD_LIBRARY_PATH="$ENV/lib:$LD_LIBRARY_PATH"
rm -f data/devices.json   # detect the GPU of this node, not the one of an earlier job
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
python -u tester.py
