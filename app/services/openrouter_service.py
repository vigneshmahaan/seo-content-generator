import httpx
from app.config.settings import Settings
from app.services.ai_exceptions import AIProviderError


class OpenRouterService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"

    async def generate(self, prompt: str) -> str:
        from app.config.config_manager import ConfigManager
        api_key = ConfigManager.get("openrouter_api_key") or self.settings.openrouter_api_key
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/aravindh/seo-content-generator",
            "X-Title": "SEO Content Generator",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "meta-llama/llama-3.1-70b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert SEO copywriter creating persuasive, human-sounding marketing content.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 450,
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.endpoint, json=payload, headers=headers)
                response.raise_for_status()
                body = response.json()
                
                choices = body.get("choices", [])
                if not choices:
                    raise AIProviderError("OpenRouter returned no choices")
                
                message = choices[0].get("message", {})
                content = message.get("content", "").strip()
                
                if not content:
                    raise AIProviderError("OpenRouter returned empty content")
                
                return content
        except httpx.HTTPStatusError as exc:
            raise AIProviderError(f"OpenRouter request failed: {exc.response.status_code} - {exc.response.text}") from exc
        except httpx.TimeoutException as exc:
            raise AIProviderError(f"OpenRouter request timeout: {exc}") from exc
        except Exception as exc:
            raise AIProviderError(f"OpenRouter request failed: {exc}") from exc
