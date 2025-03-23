from pathlib import Path
from typing import Any, cast

from tinydb import Query, TinyDB


class DBTiny:
    def __init__(self, db_dir: Path, db_file_prefix: str):
        self._db = TinyDB(
            path=db_dir / f"{db_file_prefix}.json",
            create_dirs=True
        )

    def create(self, item: dict) -> int:
        return cast(int, self._db.insert(item))

    def get(self, idx: int | list[int]) -> dict | list[dict]:
        if isinstance(idx, int):
            return cast(dict, self._db.get(doc_id=idx))
        return [{**doc, "id": doc.doc_id} for doc in self._db.get(doc_ids=idx)]

    def read_all(self) -> list[dict]:
        return [{**doc, "id": doc.doc_id} for doc in self._db.all()]

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
