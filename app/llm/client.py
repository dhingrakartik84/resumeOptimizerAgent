import asyncio
import logging
from typing import TypeVar

from ollama import AsyncClient
from pydantic import BaseModel, ValidationError

from app.core.config import settings


logger = logging.getLogger(__name__)


T = TypeVar(
    "T",
    bound=BaseModel,
)


class OllamaClient:

    def __init__(self) -> None:

        self.client = AsyncClient(
            host=settings.ollama_base_url,
            timeout=settings.ollama_timeout_seconds,
        )

        self.model = settings.ollama_model


    async def structured_chat(
        self,
        messages: list[dict],
        response_model: type[T],
        max_attempts: int = 2,
    ) -> T:

        last_exception: Exception | None = None

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            try:

                response = await self.client.chat(
                    model=self.model,
                    messages=messages,

                    format=(
                        response_model
                        .model_json_schema()
                    ),

                    stream=False,

                    options={
                        "temperature": 0,
                    },
                )

                return response_model.model_validate_json(
                    response.message.content
                )

            except (
                ValidationError,
                ValueError,
            ) as exc:

                last_exception = exc

                logger.warning(
                    "Invalid Ollama structured output. "
                    "Attempt %s of %s",
                    attempt,
                    max_attempts,
                )

                if attempt < max_attempts:
                    await asyncio.sleep(0.5)

        raise RuntimeError(
            "Ollama failed to return valid structured output."
        ) from last_exception


ollama_client = OllamaClient()