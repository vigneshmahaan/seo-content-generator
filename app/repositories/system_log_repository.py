from typing import Optional
from datetime import datetime, timezone
from app.database.client import SupabaseClient
from app.models.system_log import SystemLog


class SystemLogRepository:
    def __init__(self, client: SupabaseClient) -> None:
        self.client = client
        self.table = "system_logs"

    async def log(
        self,
        request_id: Optional[int],
        log_type: str,
        message: str,
        provider: Optional[str] = None,
    ) -> SystemLog:
        payload = {
            "request_id": request_id,
            "log_type": log_type,
            "message": message,
            "provider": provider,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        record = await self.client.insert(self.table, payload)
        return SystemLog(**record)
