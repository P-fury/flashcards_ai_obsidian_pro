import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env', '.env-chatgpt'))

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": """
            Jesteś trenerem programowania w python. Potrafisz przygotowywać flashards na podstawie przesłanych danych. Flashcard powinień być generowany wg schematu w formacie json na podstawie pliku markdown który ci prześlę:
            {
             difficulty_level: DifficultyEnum,
                tags: list[NonEmptyString],
                front_side: NonEmptyString,
                back_side: NonEmptyString,
            }
            
            DifficultyEnum:    easy, medium, hard
            
            tags: są będą w pliku markdown, który prześlę,  w format #<tag>
            front_side: pytanie
            back_side: odpowiedż 
            
            wynikiem ma być czysty kod w json.
            """},
        {
            "role": "user",
            "content": """
**📝 1. Pytest i Testy Jednostkowe**

  

**🔹 Podstawy pytest**

• pytest to popularna biblioteka do testowania w Pythonie.

• Obsługuje **testy jednostkowe** (unit tests), **testy integracyjne** i **test-driven development (TDD)**.

**🔹 Instalacja**

```sh

pip install pytest

```

**🔹 Pisanie testów jednostkowych**

```python

def add(x, y):
    return x + y

def test_add():
    assert add(2, 3) == 5
    
```

**🔹 Uruchamianie testów**

```sh

pytest test_file.py  # Uruchomienie konkretnego pliku
pytest               # Uruchomienie wszystkich testów
pytest -v            # Szczegółowy output

```
#pytest"""
        }
    ]
)

print(completion.choices[0].message.content)
