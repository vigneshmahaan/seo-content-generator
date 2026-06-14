import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from app.config.settings import Settings
from app.services.seo_service import SEOService


class AppScheduler:
    def __init__(
        self,
        seo_service: SEOService,
        settings: Settings,
        logger: logging.Logger,
    ) -> None:
        self.seo_service = seo_service
        self.settings = settings
        self.logger = logger
        self.scheduler = AsyncIOScheduler(timezone="UTC")

    def start(self) -> None:
        interval_seconds = self.settings.scheduler_interval_seconds
        if interval_seconds and interval_seconds > 0:
            trigger = IntervalTrigger(seconds=interval_seconds)
            interval_text = f"{interval_seconds} seconds"
        else:
            trigger = IntervalTrigger(minutes=self.settings.scheduler_interval_minutes)
            interval_text = f"{self.settings.scheduler_interval_minutes} minutes"

        self.scheduler.add_job(
            self.seo_service.process_pending_requests,
            trigger=trigger,
            id="seo_content_job",
            replace_existing=True,
            next_run_time=datetime.utcnow(),
        )
        self.scheduler.start()
        self.logger.info(
            "Scheduler started, running every %s",
            interval_text,
        )

    async def run_forever(self) -> None:
        self.start()
        await asyncio.Event().wait()
