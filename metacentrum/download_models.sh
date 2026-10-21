#!/bin/bash
#PBS -N download_models
#PBS -l select=1:ncpus=2:mem=8gb
#PBS -l walltime=08:00:00
#PBS -j oe
# Downloads the models in data/models.json into models/. Run from the repo root: qsub metacentrum/download_models.sh
# Needs a Python environment with huggingface_hub (see metacentrum/README.md).
set -e
cd "$PBS_O_WORKDIR"
export HF_XET_CHUNK_CACHE_SIZE_BYTES=0   # no extra chunk cache in the home directory
.venv/bin/python -u download_models.py
