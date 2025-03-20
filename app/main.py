import logging.config
import os.path
from pathlib import Path
from pprint import pprint

from app.ai.card_gen import CardGen
from app.logging_setup import setup_logging
from app.notes_reader.notes_loader import MarkdownNotesLoader
from tests.notes_reader.test_notes_loader import notes_loader

logger = logging.getLogger(__name__)

# _dirname = Path(__file__).parent

def main() -> None:
    setup_logging()

    notes_loader = MarkdownNotesLoader(os.path.join("..", "obsidian_vault"), {"python", "docker", "pytest"})
    notes = notes_loader.load()

    clientAI = CardGen(model="gpt-4o-mini")

    cards = []

    for note in notes:
        flashcards = clientAI.create_card_json(note.content)
        cards.append(flashcards.choices[0].message.content)

    pprint(cards)


if __name__ == "__main__":
    main()
