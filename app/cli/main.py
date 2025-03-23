import time
from typing import Iterator

import typer
from rich.table import Table
from typer import Typer
from rich import print
from rich.console import Console

from app.controllers.create_cards import create_cards


app: Typer = Typer(add_completion=False)
console: Console = Console()


@app.callback(invoke_without_command=True)
def menu() -> None:
    print("Choose option:")
    print("1. Create cards from Vault")
    print("2. Get cards from DB")

    choice = typer.prompt("Provide option number", type=int)

    if choice == 1:
        create_cards_cli()
        option = typer.confirm("Save to db?")
        if option:
            ...
        menu()
    else:
        print("Thank you for using Flashcards AI")


@app.command(name="save-cards")
def save_cards_cli():
    ...


def flat_if(cards: list) -> Iterator:
    for card in cards:
        if not isinstance(card, dict):
            yield from flat_if(card)
        else:
            yield card


@app.command(name="create-cards")
def create_cards_cli() -> None:
    total = 100
    with typer.progressbar(range(total), label="Generating...") as progress:
        for _ in progress:
            time.sleep(0.05)

    cards = create_cards()
    table = Table("Question", "Level", title="Flashcards AI")

    with typer.progressbar(range(100), label="Transforming...") as progress:
        for _ in progress:
            time.sleep(0.05)

    for card in cards:
        table.add_row(card.front_side, card.difficulty_level.value)

    console.print(table)