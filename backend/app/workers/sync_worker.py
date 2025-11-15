from __future__ import annotations

import asyncio

from app.services import sync as sync_service


async def reconcile_operations(events: list[dict]) -> None:
    for event in events:
        await sync_service.push_operations(event["tenant_id"], event["payload"])


if __name__ == "__main__":
    asyncio.run(reconcile_operations([]))
