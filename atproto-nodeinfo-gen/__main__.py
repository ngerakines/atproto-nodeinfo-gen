from typing import AsyncIterator
import asyncio
import argparse
import logging
import json
import httpx
from atproto import AsyncClient, CAR

logger = logging.getLogger(__name__)


async def list_repos(
    client: AsyncClient, limit: int = 100, max: int = 1000, skip_inactive: bool = False
) -> AsyncIterator[str]:
    cursor = None
    count = 0
    while count < max:
        results = await client.com.atproto.sync.list_repos(
            {"cursor": cursor, "limit": limit}
        )

        if not results.repos:
            break

        cursor = results.cursor
        for result in results.repos:
            count += 1
            if skip_inactive and result.active is False:
                continue
            yield result.did


async def main() -> None:
    parser = argparse.ArgumentParser(
        prog="atproto-nodeinfo-gen",
        description="Generate a well-known nodeinfo file for a PDS.",
    )
    parser.add_argument(
        "hostname", help="The hostname of the PDS to generate the file for."
    )
    parser.add_argument("-n", "--name", help="The name of the PDS.")
    parser.add_argument("-d", "--description", help="The description of the PDS.")
    parser.add_argument(
        "-o",
        "--out",
        default="nodeinfo",
        help="The destination that the well-known data is written to.",
    )
    args = parser.parse_args()

    name = args.name or args.hostname
    description = args.description or f"The https://{args.hostname} PDS"

    software_version = "0.0.1"

    async with httpx.AsyncClient() as client:
        health_res = await client.get(f"https://{args.hostname}/xrpc/_health")
        health = health_res.json()
        if "version" in health:
            software_version = health.get("version")

    client = AsyncClient(f"https://{args.hostname}/")

    described_server = await client.com.atproto.server.describe_server()

    records: dict[str, int] = {}

    user_count = 0
    async for did in list_repos(client):
        user_count += 1

        raw_repository = await client.com.atproto.sync.get_repo({"did": did})
        car_file = CAR.from_bytes(raw_repository)
        for _, block in car_file.blocks.items():
            record_type = block.get("$type", None)
            if record_type is None:
                continue
            records[record_type] = records.get(record_type, 0) + 1

    well_known = {
        "version": "2.2",
        "instance": {
            "name": name,
            "description": description,
        },
        "software": {
            "name": "pds",
            "version": software_version,
            "repository": "https://github.com/atprotocol/pds",
        },
        "protocols": ["atprotocol"],
        "services": {"inbound": [""], "outbound": [""]},
        "openRegistrations": not described_server.invite_code_required,
        "usage": {
            "users": {"total": user_count},
            "records": records,
        },
        "metadata": {},
    }
    with open(args.out, "w") as fout:
        fout.write(json.dumps(well_known, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
