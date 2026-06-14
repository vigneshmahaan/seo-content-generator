from groq import Groq, APIError
from app.config.settings import Settings
from app.services.ai_exceptions import AIProviderError


class GroqService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate(self, prompt: str) -> str:
        from app.config.config_manager import ConfigManager
        api_key = ConfigManager.get("groq_api_key") or self.settings.groq_api_key
        client = Groq(api_key=api_key)
        try:
            message = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                max_tokens=450,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert SEO copywriter creating persuasive, human-sounding marketing content.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            if not message.choices:
                raise AIProviderError("Groq returned empty content")
            return message.choices[0].message.content.strip()
        except APIError as exc:
            raise AIProviderError(f"Groq request failed: {exc}") from exc
        except Exception as exc:
            raise AIProviderError(f"Groq request failed: {exc}") from exc

