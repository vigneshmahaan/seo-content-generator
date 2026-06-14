import asyncio
import logging
import os
import sys

# Ensure the project root is on sys.path when running python app/main.py directly.
if __name__ == "__main__" and __package__ is None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from fastapi import FastAPI
import uvicorn
from app.config import Settings
from app.utils.logger import configure_logging
from app.database.client import SupabaseClient
from app.repositories.seo_request_repository import SEORequestRepository
from app.repositories.seo_content_repository import SEOContentRepository
from app.repositories.system_log_repository import SystemLogRepository
from app.services.google_sheet_service import GoogleSheetService
from app.services.openrouter_service import OpenRouterService
from app.services.gemini_service import GeminiService
from app.services.groq_service import GroqService
from app.services.openai_service import OpenAIService
from app.services.ai_router import AIRouter
from app.services.seo_service import SEOService
from app.scheduler.scheduler import AppScheduler
from app.api.admin import create_admin_routes


async def build_application() -> tuple[AppScheduler, SupabaseClient]:
    settings = Settings()
    logger = configure_logging(settings)

    supabase_client = SupabaseClient(settings)
    request_repository = SEORequestRepository(supabase_client)
    content_repository = SEOContentRepository(supabase_client)
    log_repository = SystemLogRepository(supabase_client)

    sheet_service = GoogleSheetService(settings)
    openrouter_service = OpenRouterService(settings)
    gemini_service = GeminiService(settings)
    groq_service = GroqService(settings)
    openai_service = OpenAIService(settings)
    ai_router = AIRouter(openrouter_service, gemini_service, groq_service, openai_service, log_repository)

    seo_service = SEOService(
        sheet_service,
        request_repository,
        content_repository,
        ai_router,
        log_repository,
        logger,
    )
    scheduler = AppScheduler(seo_service, settings, logger)
    return scheduler, supabase_client, logger


async def run_scheduler(scheduler: AppScheduler, supabase_client: SupabaseClient):
    """Run the scheduler in a separate task."""
    try:
        await scheduler.run_forever()
    finally:
        await supabase_client.close()


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="SEO Content Generator",
        description="Automated SEO content generation with Google Sheets integration",
        version="1.0.0",
    )
    return app


async def main() -> None:
    scheduler, supabase_client, logger = await build_application()
    
    # Create FastAPI app
    app = create_app()
    create_admin_routes(app, logger)
    
    # Run scheduler and API server concurrently
    try:
        # Start scheduler in background task
        scheduler_task = asyncio.create_task(run_scheduler(scheduler, supabase_client))
        
        # Run Uvicorn server
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
        )
        server = uvicorn.Server(config)
        
        logger.info("🚀 Admin panel available at http://localhost:8000/admin")
        logger.info("📊 API available at http://localhost:8000/api/config")
        
        # Run both concurrently
        await server.serve()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        scheduler_task.cancel()
        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass
    finally:
        await supabase_client.close()


if __name__ == "__main__":
    asyncio.run(main())
