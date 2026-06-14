import httpx
from app.config.settings import Settings
from typing import Any, Dict, Optional


class SupabaseClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.base_url = f"{settings.supabase_url}/rest/v1"
        self.headers = {
            "apikey": settings.supabase_key,
            "Authorization": f"Bearer {settings.supabase_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=30.0)

    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post(
            f"/{table}",
            json=payload,
            headers={**self.headers, "Prefer": "return=representation"},
        )
        response.raise_for_status()
        data = response.json()
        return data[0] if isinstance(data, list) and data else data

    async def update(self, table: str, payload: Dict[str, Any], filter_clause: str) -> None:
        response = await self.client.patch(
            f"/{table}?{filter_clause}",
            json=payload,
            headers={**self.headers, "Prefer": "return=minimal"},
        )
        response.raise_for_status()

    async def select(self, table: str, query: str) -> Any:
        response = await self.client.get(f"/{table}?{query}")
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self.client.aclose()
