from pathlib import Path
import json

from bash import bash
from constants import DATA_DIRECTORY

INDEX_FILE = str(Path(f"{DATA_DIRECTORY}/.index.json").absolute())

# Check and create index file
if not Path(INDEX_FILE).exists():
    bash(f"echo '[]' > {INDEX_FILE}")

# Check if video with specified id already in index
def index_has(id: str) -> bool:
    with open(INDEX_FILE, "r") as indexfile:
        index = json.load(indexfile)
    return id in index


# Adds video with specified id to index
def index_add(id: str):
    with open(INDEX_FILE, "r") as indexfile:
        index = json.load(indexfile)

    index.append(id)

    with open(INDEX_FILE, "w") as indexfile:
        json.dump(index, indexfile)