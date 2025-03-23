from app.db.db import DBTiny
from app.models.flashcard_models import FlashCardSrc
from app.settings.settings import dirname_app


def save_cards(cards: list[FlashCardSrc]) -> None:
    with  DBTiny(dirname_app / '.store', 'flashcards') as db:
        for card in cards:
            db.create(card.to_dict())
