#!/bin/bash
#PBS -N compare_backends
#PBS -q gpu
#PBS -l select=1:ncpus=8:ngpus=1:gpu_mem=40gb:mem=96gb:scratch_local=300gb
#PBS -l walltime=10:00:00
#PBS -j oe
# Runs tester.py twice on the same GPU, first with CUDA, then with Vulkan, from a copy of the repo and
# of all models on the node's local scratch disk. Results and timings go to results/metacentrum/.
# Needs .conda-gpu (setup_gpu_env.sh) and .conda-vulkan (setup_vulkan_env.sh).
# Run from the repo root: qsub metacentrum/compare_backends.sh
set -e
REPO="$PBS_O_WORKDIR"
WORK="$SCRATCHDIR/run"
OUT="$REPO/results/metacentrum/${PBS_JOBID%%.*}"
mkdir -p "$OUT" "$WORK"
SUMMARY="$OUT/summary.txt"
log() { echo "$(date '+%F %T') $*" | tee -a "$SUMMARY"; }

log "node $(hostname), GPU assigned by the scheduler: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi --query-gpu=index,uuid,name,memory.total,driver_version --format=csv | tee -a "$SUMMARY"

# --- the allocated GPU as Vulkan sees it; Vulkan ignores CUDA_VISIBLE_DEVICES ---
if [[ "$CUDA_VISIBLE_DEVICES" == GPU-* ]]; then UUID="${CUDA_VISIBLE_DEVICES%%,*}"
else UUID=$(nvidia-smi -i "${CUDA_VISIBLE_DEVICES%%,*}" --query-gpu=uuid --format=csv,noheader); fi
UUID="${UUID#GPU-}"
ICD=""
for f in /usr/share/vulkan/icd.d/nvidia_icd.json /etc/vulkan/icd.d/nvidia_icd.json; do [ -f "$f" ] && ICD="$f" && break; done
if [ -z "$ICD" ] && ldconfig -p | grep -q libGLX_nvidia.so.0; then
    # no ICD file on the node, but the driver library is there: describe it ourselves
    ICD="$SCRATCHDIR/nvidia_icd.json"
    echo '{"file_format_version": "1.0.1", "ICD": {"library_path": "libGLX_nvidia.so.0", "api_version": "1.3"}}' > "$ICD"
fi
VK_INDEX=""
if [ -n "$ICD" ]; then
    export VK_DRIVER_FILES="$ICD" VK_ICD_FILENAMES="$ICD"
    # vulkaninfo lists the GPUs as GPU0, GPU1, ... with their deviceUUID, in the order ggml numbers them
    VK_INDEX=$(env PATH="$REPO/.conda-vulkan/bin:$PATH" LD_LIBRARY_PATH="$REPO/.conda-vulkan/lib" vulkaninfo --summary 2>/dev/null |
        awk -v uuid="$UUID" '/^GPU[0-9]+:/ {gpu = substr($1, 4, length($1) - 4)} /deviceUUID/ && tolower($3) == tolower(uuid) {print gpu}')
fi
if [ -z "$VK_INDEX" ]; then log "Vulkan: the allocated GPU was not found (ICD: ${ICD:-none}), only CUDA will run"
else log "Vulkan: allocated GPU $UUID is Vulkan device $VK_INDEX (ICD: $ICD)"; fi

# --- copy the repo and the models to the local scratch disk ---
cd "$REPO"
git ls-files | grep -v '^models/' | tar -cf - -T - | tar -xf - -C "$WORK"
mkdir -p "$WORK/models"
log "copying $(ls models/*.gguf | wc -l) models ($(du -sh models | cut -f1)) to scratch"
start=$SECONDS
ls models/*.gguf | xargs -P 4 -I{} cp {} "$WORK/models/"
log "copy took $(( (SECONDS - start) / 60 )) min $(( (SECONDS - start) % 60 )) s"

# --- one pass per backend, same GPU, same files ---
cd "$WORK"
run() {  # run <name> <conda env>
    local prefix="$REPO/$2" start=$SECONDS
    rm -f data/devices.json
    log "$1: start"
    env PATH="$prefix/bin:$PATH" LD_LIBRARY_PATH="$prefix/lib:$LD_LIBRARY_PATH" \
        python -u tester.py "$OUT/jailbreak_$1.csv" > "$OUT/tester_$1.log" 2>&1 || log "$1: tester.py failed, see tester_$1.log"
    log "$1: took $(( (SECONDS - start) / 60 )) min $(( (SECONDS - start) % 60 )) s, $(grep -m1 'Using default device' "$OUT/tester_$1.log")"
}
run cuda .conda-gpu
if [ -n "$VK_INDEX" ]; then export GGML_VK_VISIBLE_DEVICES="$VK_INDEX"; run vulkan .conda-vulkan; fi
log "done, results in $OUT"
