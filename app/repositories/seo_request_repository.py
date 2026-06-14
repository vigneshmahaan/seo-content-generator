from typing import Dict, Optional
from app.database.client import SupabaseClient
from app.models.seo_request import SEORequest


class SEORequestRepository:
    def __init__(self, client: SupabaseClient) -> None:
        self.client = client
        self.table = "seo_requests"

    async def create(self, payload: Dict[str, Optional[str]]) -> SEORequest:
        record = await self.client.insert(self.table, payload)
        return SEORequest(**record)

    async def update_status(
        self,
        request_id: int,
        status: str,
        provider_used: Optional[str] = None,
    ) -> None:
        payload = {"status": status}
        if provider_used:
            payload["provider_used"] = provider_used
        await self.client.update(self.table, payload, f"id=eq.{request_id}")
