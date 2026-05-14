"""
src/utils/llm_client.py
Google Gemini API client wrapper (via google-genai SDK).
All LLM calls go through here — keeps services decoupled from SDK specifics.
"""
import google.generativeai as genai
from loguru import logger

from src.configs.settings import settings
from src.errorcodes.errors import ErrorCode
from src.schemas.exceptions import ChatException


class LLMClient:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self._model = genai.GenerativeModel(
            model_name=settings.LLM_MODEL,
            generation_config=genai.GenerationConfig(
                max_output_tokens=settings.LLM_MAX_TOKENS,
                temperature=settings.LLM_TEMPERATURE,
            ),
        )

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int | None = None,
    ) -> str:
        """Send a message to Gemini and return the text response."""
        try:
            # Gemini combines system prompt + user message in a single turn
            full_prompt = f"{system_prompt}\n\n{user_message}"
            response = await self._model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            logger.exception(f"LLM API call failed: {e}")
            raise ChatException(
                error_code=ErrorCode.LLM_CALL_FAILED,
                detail=str(e),
                status_code=502,
            )


llm_client = LLMClient()
