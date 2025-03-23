import logging
import os
from pathlib import Path
from typing import Any

import dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from app.tools.open_file import open_file

logger = logging.getLogger(__name__)


class CardGen:
    system_prompt_path: Path = Path(__file__).parent.resolve() / 'prompts'

    def __new__(cls, *args:Any, **kwargs:Any) -> "CardGen":
        dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env', '.env-chatgpt'))
        if os.getenv("OPENAI_API_KEY", None) is None:
            raise EnvironmentError("OPENAI_API_KEY environment variable not set")

        return super().__new__(cls)

    def __init__(self, model: str = 'gpt-3.5-turbo-16k', response_format: dict[str, str] | None = None) -> None:
        self.response_format = response_format or {"type": "json_object"}
        self.client: OpenAI = OpenAI()
        self.model = model

    def create_card_json(self, user_prompt: str) -> Any:
        messages : list[ChatCompletionMessageParam] = [
            {"role": "system", "content": open_file(type(self).system_prompt_path / "system_prompt.txt")},
            {"role": "user", "content": "Provide a JSON response with the following data: " + user_prompt},
        ]

        logger.info(f'Creating card json for user: {len(user_prompt.split())}')

        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format=self.response_format,
        )
