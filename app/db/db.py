from pathlib import Path
from typing import cast, Any

from tinydb import TinyDB, Query


class DBTiny:
    def __init__(self, db_dir: Path, db_file_prefix: str):
        self._db = TinyDB(
            db_path=db_dir / f"{db_file_prefix}.json",
            create_dirs=True
        )

    def create(self, item: dict) -> int:
        return cast(int, self._db.insert(item))

    def read(self, idx: int) -> dict:
        return cast(dict, self._db.get(doc_id=idx))

    def read_all(self) -> list[dict]:
        return cast(list[dict], self._db.all())

    def filter(self, **kwargs) -> list:
        query = Query()

        for k, v in kwargs.items():
            query &= query[k] == v
        return self._db.search(query)

    def count(self) -> int:
        return len(self._db)

    def __enter__(self) -> "DBTiny":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._db.close()
