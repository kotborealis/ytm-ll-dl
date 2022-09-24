from enum import Enum
from pathlib import Path
import dbm
from collections import namedtuple
from typing import Optional

IndexFn = namedtuple('IndexFn', 'get add')

class IndexStatus(Enum):
    ready = "ready"
    failed = "failed"


def Index(data_dir: Path) -> IndexFn:
    index_file = (data_dir / ".index").absolute()
    
    db = dbm.open(str(index_file), 'c')

    # Check if video with specified id already in index
    def get(id: str) -> Optional[IndexStatus]:
        if id.encode() not in db.keys():
            return None

        return IndexStatus[db[id].decode()]

    # Adds video with specified id to index
    def add(id: str, status: IndexStatus):
        db[id] = status.value
            
    return IndexFn(get=get, add=add)
