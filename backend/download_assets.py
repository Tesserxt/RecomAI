from pathlib import Path

from huggingface_hub import hf_hub_download

ROOT = Path(__file__).resolve().parents[1]
REPO_ID = "radha84/recomai-assets"

assets = [
    ("movies(stemd).csv", ROOT / "data"),
    ("tfidf_X_stemmed.npz", ROOT / "artifacts"),
]

for filename, directory in assets:
    directory.mkdir(parents=True, exist_ok=True)

    hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        repo_type="dataset",
        local_dir=directory,
    )

    print(f"Downloaded: {filename}")
