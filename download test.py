# import os
# import subprocess
#
# try:
#     from huggingface_hub import get_collection, snapshot_download
# except ImportError:
#     print("Installing huggingface_hub...")
#     subprocess.check_call(["pip", "install", "-U", "huggingface_hub[cli]"])
#     from huggingface_hub import get_collection, snapshot_download
#
# # --- CONFIGURATION ---
# # Replace this with the EXACT string from your URL bar (e.g. "vladikxyz/llm-based-npcs-1234abcd")
# COLLECTION_URL_SLUG = "vladikxyz/test"
# DOWNLOAD_DIR = "./skibidi"
#
# # The specific quantization you want to download.
# # You can change this if you use Q5_K_M or Q8_0 instead.
# QUANT_PATTERN = "*Q4_K_M.gguf"
#
# # ---------------------
#
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)
#
# try:
#     print(f"Fetching collection: {COLLECTION_URL_SLUG}")
#     collection = get_collection(COLLECTION_URL_SLUG)
# except Exception as e:
#     print(f"Failed to fetch collection. Is it private? You may need to run 'huggingface-cli login' first. Error: {e}")
#     exit(1)
#
# print(f"Found {len(collection.items)} models in the collection.")
#
# for item in collection.items:
#     repo_id = item.item_id
#     print(f"\nDownloading {QUANT_PATTERN} from {repo_id}...")
#
#     try:
#         # snapshot_download with allow_patterns ensures we ONLY grab the specific GGUF file,
#         # preventing it from downloading hundreds of GBs of unnecessary tensor files.
#         snapshot_download(
#             repo_id=repo_id,
#             allow_patterns=[QUANT_PATTERN],
#             local_dir=DOWNLOAD_DIR,
#             local_dir_use_symlinks=False  # Forces actual files, not symlinks, making them easier to manage
#         )
#         print(f"✅ Success: {repo_id}")
#     except Exception as e:
#         print(f"❌ Failed to download {repo_id}. It might not have a {QUANT_PATTERN} file. Error: {e}")
#
# print("\n🎉 All downloads complete!")
import json

with open("data/models.json", "r") as f:
    mods = json.load(f)
print(len(mods))