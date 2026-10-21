"""Downloads the .gguf files listed in data/models.json from our Hugging Face collection into models/.

    python download_models.py --dry-run   # only list what would be downloaded and how big it is
    python download_models.py             # download every file that is not in models/ yet

Needs: pip install -U "huggingface_hub[hf_xet]"
"""
import json
import os
import shutil
import sys

from huggingface_hub import HfApi, get_collection, hf_hub_download

COLLECTION = "vladikxyz/llm-based-npcs-6a6a3825158124a75e068dd9"
MODELS_FILE = "data/models.json"
MODELS_DIR = "models"


def find_files(api, wanted):
    """Map every wanted file name to (repo, path in the repo, size) by looking through the collection."""
    found = {}
    for item in get_collection(COLLECTION).items:
        if item.item_type != "model": continue
        for entry in api.list_repo_tree(item.item_id, recursive=True):
            name = os.path.basename(entry.path)
            if name in wanted and name not in found:
                found[name] = (item.item_id, entry.path, getattr(entry, "size", 0) or 0)
    return found


def main(dry_run):
    with open(MODELS_FILE) as f:
        wanted = {os.path.basename(m["path"]) for m in json.load(f)}
    api = HfApi()
    found = find_files(api, wanted)
    missing = sorted(wanted - set(found))
    todo = {name: info for name, info in sorted(found.items()) if not os.path.exists(os.path.join(MODELS_DIR, name))}

    print(f"{len(wanted)} files in {MODELS_FILE}: {len(found)} found in the collection, "
          f"{len(found) - len(todo)} already in {MODELS_DIR}/, {len(todo)} to download "
          f"({sum(size for _, _, size in todo.values()) / 1e9:.1f} GB)")
    for name in missing: print(f"  NOT IN THE COLLECTION: {name}")
    for name, (repo, path, size) in todo.items(): print(f"  {size / 1e9:6.1f} GB  {name}  ({repo})")
    if dry_run: return

    os.makedirs(MODELS_DIR, exist_ok=True)
    for i, (name, (repo, path, size)) in enumerate(todo.items(), 1):
        print(f"[{i}/{len(todo)}] {name} ({size / 1e9:.1f} GB)", flush=True)
        try:
            local = hf_hub_download(repo_id=repo, filename=path, local_dir=MODELS_DIR)
            # files that sit in a folder of the repo are moved next to the others
            if os.path.abspath(local) != os.path.abspath(os.path.join(MODELS_DIR, name)):
                shutil.move(local, os.path.join(MODELS_DIR, name))
        except Exception as e:
            print(f"  FAILED: {e}", flush=True)
    print("Done.")


if __name__ == '__main__':
    main("--dry-run" in sys.argv)
