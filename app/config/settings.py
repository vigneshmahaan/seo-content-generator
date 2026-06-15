from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY")
    google_sheet_id: str = Field(..., env="GOOGLE_SHEET_ID")
    google_credentials_file: str = Field(..., env="GOOGLE_CREDENTIALS_FILE")
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    custom_prompt_template: str = Field(
        "Write a single SEO-optimized marketing paragraph between 150 and 250 words.\nUse persuasive, human-written language with a strong call-to-action.\nPlace the keywords naturally and avoid robotic phrasing.\nKeep readability high, vary sentence structure, and provide a unique introduction and closing.",
        env="CUSTOM_PROMPT_TEMPLATE"
    )
    gemini_api_url: str = Field(
        "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generate",
        env="GEMINI_API_URL",
    )
    groq_api_url: str = Field(
        "https://api.groq.ai/v1/models/groq-1/outputs",
        env="GROQ_API_URL",
    )
    openai_api_url: str = Field(
        "https://api.openai.com/v1/chat/completions",
        env="OPENAI_API_URL",
    )
    sheet_range: str = Field("A2:E", env="SHEET_RANGE")
    scheduler_interval_minutes: int = Field(5, env="SCHEDULER_INTERVAL_MINUTES")
    scheduler_interval_seconds: int = Field(20, env="SCHEDULER_INTERVAL_SECONDS")
    log_file: str = Field("logs/app.log", env="LOG_FILE")
    log_max_bytes: int = Field(10_485_760, env="LOG_MAX_BYTES")
    log_backup_count: int = Field(5, env="LOG_BACKUP_COUNT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **data):
        """Initialize settings, with config.json values overriding env vars."""
        super().__init__(**data)
        
        # Override with config.json values if they exist
        try:
            from app.config.config_manager import ConfigManager
            runtime_config = ConfigManager.load()
            
            if runtime_config.get("google_sheet_id"):
                self.google_sheet_id = runtime_config["google_sheet_id"]
            if runtime_config.get("openrouter_api_key"):
                self.openrouter_api_key = runtime_config["openrouter_api_key"]
            if runtime_config.get("gemini_api_key"):
                self.gemini_api_key = runtime_config["gemini_api_key"]
            if runtime_config.get("groq_api_key"):
                self.groq_api_key = runtime_config["groq_api_key"]
            if runtime_config.get("openai_api_key"):
                self.openai_api_key = runtime_config["openai_api_key"]
            if runtime_config.get("custom_prompt_template"):
                self.custom_prompt_template = runtime_config["custom_prompt_template"]
            if runtime_config.get("scheduler_interval_seconds"):
                self.scheduler_interval_seconds = runtime_config["scheduler_interval_seconds"]
        except Exception:
            # ConfigManager not available yet, use defaults from env
            pass
