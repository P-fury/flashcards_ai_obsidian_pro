from typing import Iterator

import typer
from rich.table import Table
from typer import Typer

from rich import print
from rich.console import Console

from app.controllers.create_cards import create_cards

app: Typer = typer.Typer()
console: Console = Console()


@app.command()
def run() -> None:
    print('Flashcards AI')


def flat_if(cards: list) -> Iterator:
    for card in cards:
        if not isinstance(card, dict):
            yield from flat_if(card)
        else:
            yield card


@app.command(name="create-cards")
def create_cards_cli() -> None:
    cards = create_cards()
    table = Table("Question", "Level", title='Flashcards AI')

    for card in flat_if(cards):
        table.add_row(card["front_side"], card["difficulty_level"])

    console.print(table)
