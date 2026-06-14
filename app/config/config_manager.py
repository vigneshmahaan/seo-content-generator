import json
import os
from typing import Dict, Any
from pathlib import Path


class ConfigManager:
    """Manage runtime configuration stored in JSON file."""
    
    CONFIG_FILE = "config.json"
    
    # Default configuration
    DEFAULTS = {
        "google_sheet_id": "",
        "openrouter_api_key": "",
        "gemini_api_key": "",
        "groq_api_key": "",
        "openai_api_key": "",
        "scheduler_interval_seconds": 20,
    }
    
    @classmethod
    def load(cls) -> Dict[str, Any]:
        """Load configuration from JSON file or return defaults."""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**cls.DEFAULTS, **config}
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return cls.DEFAULTS.copy()
        return cls.DEFAULTS.copy()
    
    @classmethod
    def save(cls, config: Dict[str, Any]) -> None:
        """Save configuration to JSON file."""
        try:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to save config: {e}") from e
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a specific configuration value."""
        config = cls.load()
        return config.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a specific configuration value."""
        config = cls.load()
        config[key] = value
        cls.save(config)
    
    @classmethod
    def update(cls, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        config = cls.load()
        config.update(updates)
        cls.save(config)
