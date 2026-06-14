from datetime import datetime, timezone, timedelta
from typing import List
from urllib.parse import quote
from app.database.client import SupabaseClient
from app.models.seo_content import SEOContent


class SEOContentRepository:
    def __init__(self, client: SupabaseClient) -> None:
        self.client = client
        self.table = "seo_contents"

    async def save(self, request_id: int, generated_content: str) -> SEOContent:
        payload = {
            "request_id": request_id,
            "generated_content": generated_content,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        record = await self.client.insert(self.table, payload)
        return SEOContent(**record)

    async def fetch_recent(self, days: int = 7) -> List[str]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        encoded_datetime = quote(cutoff.isoformat(), safe="")
        query = f"generated_at=gt.{encoded_datetime}&select=generated_content"
        records = await self.client.select(self.table, query)
        return [record["generated_content"] for record in records if record.get("generated_content")]
