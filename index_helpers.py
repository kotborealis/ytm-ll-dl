from pathlib import Path
import json
from collections import namedtuple

from bash import bash

IndexFn = namedtuple('IndexFn', 'has add')


def Index(data_dir: Path) -> IndexFn:
    index_file = (data_dir / ".index.json").absolute()
    
    # Check and create index file
    if not index_file.exists():
        bash(f"echo '[]' > {str(index_file)}")

    # Check if video with specified id already in index
    def index_has(id: str) -> bool:
        with open(str(index_file), "r") as indexfile:
            index = json.load(indexfile)
        return id in index


    # Adds video with specified id to index
    def index_add(id: str):
        with open(str(index_file), "r") as indexfile:
            index = json.load(indexfile)

        index.append(id)

        with open(str(index_file), "w") as indexfile:
            json.dump(index, indexfile)
            
    return IndexFn(has=index_has, add=index_add)
