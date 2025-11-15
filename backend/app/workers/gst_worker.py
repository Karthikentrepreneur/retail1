from __future__ import annotations

import asyncio

from app.services import gst as gst_service


async def process_gst_queue(message: dict) -> None:
    tenant_id = message["tenant_id"]
    gst_payload = message["payload"]
    await gst_service.generate_einvoice(tenant_id, gst_payload)


async def main(messages: list[dict]) -> None:
    for message in messages:
        await process_gst_queue(message)


if __name__ == "__main__":
    asyncio.run(main([]))
