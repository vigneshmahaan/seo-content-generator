import asyncio
import logging
from typing import List, Optional
from app.prompts.seo_prompt import build_seo_prompt
from app.repositories.seo_request_repository import SEORequestRepository
from app.repositories.seo_content_repository import SEOContentRepository
from app.repositories.system_log_repository import SystemLogRepository
from app.services.google_sheet_service import GoogleSheetService
from app.services.ai_router import AIRouter, AIProviderError
from app.config.config_manager import ConfigManager


class SEOService:
    def __init__(
        self,
        sheet_service: GoogleSheetService,
        request_repository: SEORequestRepository,
        content_repository: SEOContentRepository,
        ai_router: AIRouter,
        log_repository: SystemLogRepository,
        logger: logging.Logger,
    ) -> None:
        self.sheet_service = sheet_service
        self.request_repository = request_repository
        self.content_repository = content_repository
        self.ai_router = ai_router
        self.log_repository = log_repository
        self.logger = logger

    async def process_pending_requests(self) -> None:
        self.logger.info("Scheduler triggered SEO content run")
        try:
            pending_rows = await self.sheet_service.fetch_pending_rows()
        except Exception as exc:
            self.logger.exception("Failed to read Google Sheets")
            await self.log_repository.log(None, "sheet_error", str(exc), None)
            return

        if not pending_rows:
            self.logger.info("No pending rows found")
            return

        for row in pending_rows:
            row_number = row["row_number"]
            request_record = None
            provider_used: Optional[str] = None
            try:
                self.logger.info("Processing row %s", row_number)
                await self.sheet_service.update_row(row_number, "", "Processing")

                if not row["input_one"] or not row["input_two"]:
                    raise ValueError("Required inputs are missing")

                # Wait 3 seconds to allow the optional input to be filled in.
                await asyncio.sleep(3)
                row = await self.sheet_service.fetch_row_data(row_number)

                if not row["input_one"] or not row["input_two"]:
                    raise ValueError("Required inputs are missing after wait")

                request_payload = {
                    "input_one": row["input_one"],
                    "input_two": row["input_two"],
                    "input_three": row.get("input_three"),
                    "status": "Processing",
                }
                request_record = await self.request_repository.create(request_payload)

                await self.log_repository.log(
                    request_record.id,
                    "request_received",
                    f"Request created for row {row_number}",
                    None,
                )

                recent_contents = await self.content_repository.fetch_recent(days=7)
                
                template = ConfigManager.get("custom_prompt_template") or self.sheet_service.settings.custom_prompt_template
                
                prompt = build_seo_prompt(
                    template,
                    row["input_one"],
                    row["input_two"],
                    row.get("input_three") or "",
                    recent_contents,
                )

                content, provider_used = await self.ai_router.generate(
                    prompt, request_record.id
                )

                await self.content_repository.save(request_record.id, content)
                
                # Update sheet with generated content BEFORE marking as Completed
                try:
                    self.logger.info("Updating sheet row %s with content", row_number)
                    await self.sheet_service.update_row(row_number, content, "Completed")
                    self.logger.info("Sheet row %s updated successfully", row_number)
                except Exception as sheet_exc:
                    self.logger.error("Failed to update sheet row %s: %s", row_number, sheet_exc)
                    # Don't raise - proceed to mark as Completed anyway
                
                # Mark as Completed ONLY after sheet update attempt
                await self.request_repository.update_status(
                    request_record.id, "Completed", provider_used
                )

                # Non-critical logging - don't fail if these have issues
                try:
                    await self.log_repository.log(
                        request_record.id,
                        "sheet_updated",
                        f"Row {row_number} updated with content and completed status",
                        provider_used,
                    )
                except Exception as log_exc:
                    self.logger.warning("Failed to log sheet update: %s", log_exc)
                
                self.logger.info(
                    "Row %s completed using provider %s",
                    row_number,
                    provider_used,
                )
            except AIProviderError as exc:
                self.logger.exception("AI generation failed for row %s", row_number)
                if request_record:
                    await self.request_repository.update_status(
                        request_record.id, "Failed", provider_used
                    )
                    await self.log_repository.log(
                        request_record.id,
                        "generation_error",
                        str(exc),
                        provider_used,
                    )
                await self._mark_failure(row_number)
            except Exception as exc:
                self.logger.exception("Processing failed for row %s", row_number)
                if request_record:
                    await self.request_repository.update_status(
                        request_record.id, "Failed", provider_used
                    )
                    await self.log_repository.log(
                        request_record.id,
                        "processing_error",
                        str(exc),
                        provider_used,
                    )
                else:
                    await self.log_repository.log(
                        None,
                        "validation_error",
                        str(exc),
                        None,
                    )
                await self._mark_failure(row_number)

    async def _mark_failure(self, row_number: int) -> None:
        try:
            await self.sheet_service.update_row(row_number, "", "Failed")
        except Exception as exc:
            self.logger.exception("Failed to update sheet status for row %s", row_number)
            await self.log_repository.log(None, "sheet_error", str(exc), None)
