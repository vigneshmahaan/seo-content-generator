from typing import Optional, Tuple
from app.repositories.system_log_repository import SystemLogRepository
from app.services.openrouter_service import OpenRouterService
from app.services.gemini_service import GeminiService
from app.services.groq_service import GroqService
from app.services.openai_service import OpenAIService
from app.services.ai_exceptions import AIProviderError


class AIRouter:
    def __init__(
        self,
        openrouter_service: OpenRouterService,
        gemini_service: GeminiService,
        groq_service: GroqService,
        openai_service: OpenAIService,
        log_repository: SystemLogRepository,
    ) -> None:
        self.providers = [
            ("OpenRouter", openrouter_service),
            ("Groq", groq_service),
            ("Gemini", gemini_service),
            # ("OpenAI", openai_service),  # Disabled - account has no quota
        ]
        self.log_repository = log_repository

    async def generate(
        self, prompt: str, request_id: Optional[int] = None
    ) -> Tuple[str, str]:
        last_exception: Optional[Exception] = None
        import logging
        logger = logging.getLogger(__name__)
        
        for provider_name, service in self.providers:
            try:
                logger.info(f"Attempting provider: {provider_name}")
                await self.log_repository.log(
                    request_id,
                    "provider_selected",
                    f"Trying provider {provider_name}",
                    provider_name,
                )
                content = await service.generate(prompt)
                await self.log_repository.log(
                    request_id,
                    "content_generated",
                    f"Generated content using {provider_name}",
                    provider_name,
                )
                return content, provider_name
            except AIProviderError as exc:
                last_exception = exc
                logger.error(f"{provider_name} failed: {exc}")
                await self.log_repository.log(
                    request_id,
                    "provider_failed",
                    f"{provider_name} failed: {exc}",
                    provider_name,
                )
                continue
            except Exception as exc:
                last_exception = AIProviderError(f"{provider_name} failed with unexpected error: {exc}")
                logger.error(f"{provider_name} unexpected error: {exc}", exc_info=True)
                await self.log_repository.log(
                    request_id,
                    "provider_failed",
                    f"{provider_name} failed: {exc}",
                    provider_name,
                )
                continue
        raise AIProviderError(
            f"All AI providers failed. Last error: {last_exception}"
        ) from last_exception
