from dataclasses import dataclass
from enum import Enum


class DifficultyEnum(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class NonEmptyString(str):
    def __new__(cls, value)-> str:
        if not value.strip():
            raise ValueError("String cannot be empty")
        return super().__new__(cls,value)

@dataclass(frozen=True, kw_only=True, slots=True)
class FlashCard:
    difficulty_level: DifficultyEnum
    tags: list[str]
    front_site: str
    back_site: str
    origin: str

    def __post_init__(self) -> None:
        if not self.front_site:
            raise ValueError("Flashcard has to have a question.")
        if not self.back_site:
            raise ValueError("Flashcard has to have an answer.")
        if not self.tags:
            raise ValueError("Tags must be a non-empty set.")