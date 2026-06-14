import asyncio
from typing import Any, Dict, List, Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config.settings import Settings


class GoogleSheetService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.creds = Credentials.from_service_account_file(
            self.settings.google_credentials_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        self.client = build("sheets", "v4", credentials=self.creds)
        self.values_api = self.client.spreadsheets().values()

    async def fetch_pending_rows(self) -> List[Dict[str, Any]]:
        try:
            result = await asyncio.to_thread(self._fetch_range)
            rows = result.get("values", [])
            pending_rows = []
            for index, row in enumerate(rows, start=2):
                values = [cell.strip() for cell in row] + ["", "", "", "", ""]
                status = values[4] or "Pending"
                has_inputs = bool(values[0]) and bool(values[1])
                should_process = (
                    status.lower() == "pending"
                    or (status.lower() == "processing" and not values[3])
                    or (status.lower() == "failed" and not values[3] and has_inputs)
                )
                if should_process and has_inputs:
                    pending_rows.append(
                        {
                            "row_number": index,
                            "input_one": values[0],
                            "input_two": values[1],
                            "input_three": values[2],
                            "generated_content": values[3],
                            "status": status,
                        }
                    )
            return pending_rows
        except HttpError as exc:
            raise RuntimeError(f"Google Sheets read failed: {exc}") from exc

    def _fetch_range(self) -> Dict[str, Any]:
        from app.config.config_manager import ConfigManager
        sheet_id = ConfigManager.get("google_sheet_id") or self.settings.google_sheet_id
        return self.values_api.get(
            spreadsheetId=sheet_id,
            range=self.settings.sheet_range,
        ).execute()

    async def update_row(
        self, row_number: int, generated_content: str, status: str
    ) -> None:
        try:
            await asyncio.to_thread(
                self._update_range,
                row_number,
                generated_content,
                status,
            )
        except HttpError as exc:
            raise RuntimeError(f"Google Sheets update failed: {exc}") from exc

    async def fetch_row_data(self, row_number: int) -> Dict[str, Any]:
        try:
            result = await asyncio.to_thread(self._fetch_row, row_number)
            values = [cell.strip() for cell in result.get("values", [[]])[0]] + ["", "", "", "", ""]
            return {
                "row_number": row_number,
                "input_one": values[0],
                "input_two": values[1],
                "input_three": values[2],
                "generated_content": values[3],
                "status": values[4] or "Pending",
            }
        except HttpError as exc:
            raise RuntimeError(f"Google Sheets row fetch failed: {exc}") from exc

    def _fetch_row(self, row_number: int) -> Dict[str, Any]:
        from app.config.config_manager import ConfigManager
        sheet_id = ConfigManager.get("google_sheet_id") or self.settings.google_sheet_id
        return self.values_api.get(
            spreadsheetId=sheet_id,
            range=f"A{row_number}:E{row_number}",
        ).execute()

    def _update_range(
        self, row_number: int, generated_content: str, status: str
    ) -> Dict[str, Any]:
        from app.config.config_manager import ConfigManager
        sheet_id = ConfigManager.get("google_sheet_id") or self.settings.google_sheet_id
        return self.values_api.update(
            spreadsheetId=sheet_id,
            range=f"D{row_number}:E{row_number}",
            valueInputOption="RAW",
            body={"values": [[generated_content, status]]},
        ).execute()
