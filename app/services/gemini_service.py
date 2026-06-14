import google.generativeai as genai
from app.config.settings import Settings
from app.services.ai_exceptions import AIProviderError


class GeminiService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate(self, prompt: str) -> str:
        from app.config.config_manager import ConfigManager
        api_key = ConfigManager.get("gemini_api_key") or self.settings.gemini_api_key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=450,
                ),
            )
            if not response.text:
                raise AIProviderError("Gemini returned empty content")
            return response.text.strip()
        except Exception as exc:
            raise AIProviderError(f"Gemini request failed: {exc}") from exc

