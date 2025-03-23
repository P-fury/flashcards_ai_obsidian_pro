from typing import Any

from app.db.db import DBTiny
from app.settings.settings import dirname_app


def save_cards(cards: list[dict[str, Any]]) -> None:
    with  DBTiny(dirname_app/ '.store', 'flashcards') as db:
        for card in cards:
            db.create(card)
