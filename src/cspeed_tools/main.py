import asyncio
from pathlib import Path

import yaml

from cspeed_tools.bot import CSpeedBot, ServiceContainer
from cspeed_tools.config import Settings
from cspeed_tools.constants import EXPECTED_ENDPOINTS
from cspeed_tools.db.engine import Database
from cspeed_tools.db.migrations import run_migrations
from cspeed_tools.db.repositories.global_actions_repo import GlobalActionsRepository
from cspeed_tools.errors import ManifestValidationError
from cspeed_tools.logging_setup import setup_logging
from cspeed_tools.services.global_actions_service import GlobalActionsService


def validate_manifest_count() -> None:
    path = Path(__file__).with_name("manifest") / "commands_manifest.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    count = len(data["endpoints"])
    if count != EXPECTED_ENDPOINTS:
        raise ManifestValidationError(f"Expected {EXPECTED_ENDPOINTS} endpoints, found {count}")


async def runner() -> None:
    setup_logging()
    settings = Settings()
    validate_manifest_count()
    db = Database(settings.database_url)
    await db.connect()
    await run_migrations(db)
    repo = GlobalActionsRepository(db)
    services = ServiceContainer(settings, db, GlobalActionsService(repo))
    bot = CSpeedBot(services)
    await bot.start(settings.bot_token)


def main() -> None:
    asyncio.run(runner())


if __name__ == "__main__":
    main()
