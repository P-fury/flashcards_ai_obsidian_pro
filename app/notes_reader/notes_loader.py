import os
import re
from datetime import datetime
from typing import Iterable, List, override

from app.models.note_models import Note
from app.notes_reader.notes_loader_abc import NotesLoaderABC


class NotesLoader(NotesLoaderABC):
    def __init__(self, folder_path: str, tags: Iterable[str]) -> None:
        self.folder_path = folder_path
        self.tags = tags

    @override
    @property
    def folder_path(self) -> str:
        return self._folder_path

    @folder_path.setter
    def folder_path(self, folder_path: str) -> None:
        self._folder_path = folder_path

    @override
    @property
    def tags(self) -> Iterable[str]:
        return self._tags

    @tags.setter
    def tags(self, tags: Iterable[str]) -> None:
        tags_normalized = set()

        for tag in tags:
            tag_ = tag.lower().strip()
            if not tag_.startswith("#"):
                tag_ = "#" + tag_
            tags_normalized.add(tag_)  # Dodajemy zawsze, niezależnie od tego, czy zaczyna się od #
        self._tags = tags_normalized

    @staticmethod
    def __find_tags(content: str) -> set[str]:
        return set(re.findall(r"#\w+", content))

    def __check_tag(self, file_tags: set[str]) -> bool:
        return any(tag for tag in file_tags if tag in self.tags)

    @override
    def load(self) -> List[Note]:
        notes = []

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".md"):
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    file_tags = self.__find_tags(content)
                    if self.__check_tag(file_tags):
                        note = Note(
                            title=filename[:-3],
                            content=content,
                            tags=file_tags,
                            updated_at=datetime.fromtimestamp(os.path.getmtime(file_path)),
                        )
                        notes.append(note)
        return notes