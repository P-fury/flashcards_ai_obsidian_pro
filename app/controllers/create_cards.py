import logging

from app.ai.card_gen import CardGen
from app.models.flashcard_models import DifficultyEnum, FlashCardSrc, NonEmptyString
from app.models.note_models import Note
from app.notes_reader.notes_loader import MarkdownNotesLoader
from app.tools.parse_output_to_json import parse_output_to_json

logger = logging.getLogger(__name__)

def create_cards() -> list[FlashCardSrc]:
    vault_path =  "obsidian_vault"
    notes_loader = MarkdownNotesLoader(vault_path, {"docker"})
    notes = notes_loader.load()

    client_ai = CardGen(model="gpt-4o-mini")

    cards = []
    for note in notes:
        flashcards = client_ai.create_card_json(note.content)
        try:
            flashcards = parse_output_to_json(flashcards.choices[0].message.content)
        except ValueError:
            logger.exception("Failed to parse card")

        if isinstance(flashcards, list):
            for data in flashcards:
                cards.append(create_flashcard(data, note))
        elif isinstance(flashcards, dict) and "flashcards" in flashcards:
            for data in flashcards["flashcards"]:
                cards.append(create_flashcard(data, note))


    return cards


def create_flashcard(data: dict[str, str], note: Note) -> FlashCardSrc:
    return FlashCardSrc(
        difficulty_level=DifficultyEnum(data["difficulty_level"]),
        tags=[NonEmptyString(tag) for tag in note.tags],
        front_side=NonEmptyString(data["front_side"]),
        back_side=NonEmptyString(data["back_side"]),
        origin=NonEmptyString(f"{note.title}.md"),
    )