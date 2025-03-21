import logging
import os

from app.ai.card_gen import CardGen
from app.models.note_models import Note
from app.notes_reader.notes_loader import MarkdownNotesLoader
from app.settings.settings import dirname_app
from app.tools.parse_output_to_json import parse_output_to_json

logger = logging.getLogger(__name__)


def create_cards() -> list[dict]:
    notes_loader = MarkdownNotesLoader(dirname_app / '..' / 'obsidian_vault', {"docker"})
    notes: list[Note] = notes_loader.load()

    client_ai: CardGen = CardGen(model="gpt-4o-mini")

    cards = []

    for note in notes:
        flashcards = client_ai.create_card_json(note.content)

        try:
            parsed = parse_output_to_json(flashcards.choices[0].message.content)
            cards.extend(parsed.get("flashcards", []))  # <-- to spłaszcza
        except ValueError:
            logger.exception("Failed to parse card")

    return cards
