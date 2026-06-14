from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
import logging

from app.config.config_manager import ConfigManager


class ConfigUpdate(BaseModel):
    google_sheet_id: str = ""
    openrouter_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    openai_api_key: str = ""
    scheduler_interval_seconds: int = 20


def create_admin_routes(app: FastAPI, logger: logging.Logger) -> None:
    """Create admin panel routes."""
    
    @app.get("/admin", response_class=HTMLResponse)
    async def admin_panel():
        """Serve the admin configuration panel."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Content Generator - Configuration</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        textarea {
            resize: vertical;
            min-height: 60px;
        }
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 30px;
        }
        button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-save {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-save:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        .btn-reset {
            background: #f0f0f0;
            color: #333;
        }
        .btn-reset:hover {
            background: #e0e0e0;
        }
        .message {
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: none;
            font-size: 14px;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            display: block;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            display: block;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin-top: 10px;
        }
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #667eea;
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 3px;
            font-size: 13px;
            color: #004085;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚙️ Configuration Panel</h1>
        <p class="subtitle">Update your API keys and settings</p>
        
        <div class="info-box">
            ℹ️ Changes are saved immediately and take effect on the next scheduler cycle.
        </div>
        
        <div id="message" class="message"></div>
        
        <form id="configForm">
            <div class="form-group">
                <label for="googleSheetId">Google Sheet ID</label>
                <input type="text" id="googleSheetId" name="googleSheetId" placeholder="e.g., 1NzJT8JVV19zreVUkJduF_CdPatk9JxhkrYuejM9Ocio">
            </div>
            
            <div class="form-group">
                <label for="openrouterApiKey">OpenRouter API Key</label>
                <input type="password" id="openrouterApiKey" name="openrouterApiKey" placeholder="sk-or-v1-...">
            </div>
            
            <div class="form-group">
                <label for="geminiApiKey">Gemini API Key (Fallback)</label>
                <input type="password" id="geminiApiKey" name="geminiApiKey" placeholder="AQ.Ab8RN6Lu...">
            </div>
            
            <div class="form-group">
                <label for="groqApiKey">Groq API Key (Fallback)</label>
                <input type="password" id="groqApiKey" name="groqApiKey" placeholder="gsk_...">
            </div>
            
            <div class="form-group">
                <label for="openaiApiKey">OpenAI API Key (Fallback)</label>
                <input type="password" id="openaiApiKey" name="openaiApiKey" placeholder="sk-proj-...">
            </div>
            
            <div class="form-group">
                <label for="schedulerInterval">Scheduler Interval (seconds)</label>
                <input type="number" id="schedulerInterval" name="schedulerInterval" min="5" max="3600" value="20">
            </div>
            
            <div class="button-group">
                <button type="submit" class="btn-save">💾 Save Configuration</button>
                <button type="button" class="btn-reset" onclick="location.reload()">🔄 Refresh</button>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Saving configuration...</p>
            </div>
        </form>
    </div>
    
    <script>
        const form = document.getElementById('configForm');
        const messageDiv = document.getElementById('message');
        const loading = document.getElementById('loading');
        
        // Load current config
        async function loadConfig() {
            try {
                const response = await fetch('/api/config');
                if (!response.ok) throw new Error('Failed to load config');
                const config = await response.json();
                
                document.getElementById('googleSheetId').value = config.google_sheet_id || '';
                document.getElementById('openrouterApiKey').value = config.openrouter_api_key || '';
                document.getElementById('geminiApiKey').value = config.gemini_api_key || '';
                document.getElementById('groqApiKey').value = config.groq_api_key || '';
                document.getElementById('openaiApiKey').value = config.openai_api_key || '';
                document.getElementById('schedulerInterval').value = config.scheduler_interval_seconds || 20;
            } catch (error) {
                showMessage('Failed to load configuration: ' + error.message, 'error');
            }
        }
        
        // Save config
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            loading.style.display = 'block';
            messageDiv.className = 'message';
            
            const formData = new FormData(form);
            const config = {
                google_sheet_id: formData.get('googleSheetId'),
                openrouter_api_key: formData.get('openrouterApiKey'),
                gemini_api_key: formData.get('geminiApiKey'),
                groq_api_key: formData.get('groqApiKey'),
                openai_api_key: formData.get('openaiApiKey'),
                scheduler_interval_seconds: parseInt(formData.get('schedulerInterval')) || 20,
            };
            
            try {
                const response = await fetch('/api/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(config),
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to save config');
                }
                
                showMessage('✅ Configuration saved successfully! Changes take effect immediately.', 'success');
            } catch (error) {
                showMessage('❌ Error: ' + error.message, 'error');
            } finally {
                loading.style.display = 'none';
            }
        });
        
        function showMessage(text, type) {
            messageDiv.textContent = text;
            messageDiv.className = 'message ' + type;
            setTimeout(() => {
                messageDiv.className = 'message';
            }, 5000);
        }
        
        // Load config on page load
        window.addEventListener('load', loadConfig);
    </script>
</body>
</html>
        """
    
    @app.get("/api/config")
    async def get_config() -> Dict[str, Any]:
        """Get current configuration."""
        try:
            from app.config.settings import Settings
            # This loads .env and overrides with config.json
            active_settings = Settings()
            logger.info("Config retrieved via API")
            return {
                "google_sheet_id": active_settings.google_sheet_id,
                "openrouter_api_key": active_settings.openrouter_api_key,
                "gemini_api_key": active_settings.gemini_api_key,
                "groq_api_key": active_settings.groq_api_key,
                "openai_api_key": active_settings.openai_api_key,
                "scheduler_interval_seconds": active_settings.scheduler_interval_seconds,
            }
        except Exception as e:
            logger.error(f"Failed to get config: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/config")
    async def update_config(update: ConfigUpdate) -> Dict[str, str]:
        """Update configuration."""
        try:
            config_dict = update.dict(exclude_unset=False)
            ConfigManager.update(config_dict)
            logger.info("Configuration updated via API")
            return {"message": "Configuration updated successfully"}
        except Exception as e:
            logger.error(f"Failed to update config: {e}")
            raise HTTPException(status_code=500, detail=str(e))
