from dataclasses import dataclass
from enum import Enum
from typing import Any


class DifficultyEnum(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class NonEmptyString(str):
    def __new__(cls, value) -> "NonEmptyString":
        if not value.strip():
            raise ValueError("String cannot be empty")
        return super().__new__(cls, value)


@dataclass(frozen=True, kw_only=True, slots=True)
class FlashCardSrc:
    difficulty_level: DifficultyEnum
    tags: list[NonEmptyString]
    front_side: NonEmptyString
    back_side: NonEmptyString
    origin: NonEmptyString

    def __post_init__(self) -> None:
        if not self.front_side:
            raise ValueError("Flashcard has to have a question.")
        if not self.back_side:
            raise ValueError("Flashcard has to have an answer.")
        if not self.tags:
            raise ValueError("Tags must be a non-empty set.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "difficulty_level": self.difficulty_level.value,
            "tags": list(self.tags),
            "front_side": str(self.front_side),
            "back_side": str(self.back_side),
            "origin": str(self.origin),
        }


@dataclass(frozen=True, kw_only=True, slots=True)
class FlashCard(FlashCardSrc):
    id: int