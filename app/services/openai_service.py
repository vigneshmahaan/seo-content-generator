from openai import OpenAI, APIError
from app.config.settings import Settings
from app.services.ai_exceptions import AIProviderError


class OpenAIService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate(self, prompt: str) -> str:
        from app.config.config_manager import ConfigManager
        api_key = ConfigManager.get("openai_api_key") or self.settings.openai_api_key
        client = OpenAI(api_key=api_key)
        try:
            message = client.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=450,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert SEO copywriter creating persuasive, human-sounding marketing content.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            if not message.choices:
                raise AIProviderError("OpenAI returned no choices")
            content = message.choices[0].message.content
            if not content:
                raise AIProviderError("OpenAI returned empty content")
            return content.strip()
        except APIError as exc:
            raise AIProviderError(f"OpenAI request failed: {exc}") from exc
        except Exception as exc:
            raise AIProviderError(f"OpenAI request failed: {exc}") from exc

