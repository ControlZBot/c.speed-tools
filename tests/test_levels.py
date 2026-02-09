import pytest

from cspeed_tools.db.engine import Database
from cspeed_tools.db.migrations import run_migrations
from cspeed_tools.db.repositories.levels_repo import LevelsRepository
from cspeed_tools.services.level_service import LevelService


@pytest.mark.asyncio
async def test_award_xp_antispam(tmp_path) -> None:
    db = Database(f"sqlite+aiosqlite:///{tmp_path}/levels.db")
    await db.connect()
    await run_migrations(db)

    service = LevelService(LevelsRepository(db), cooldown_seconds=30)
    xp1 = await service.award_message_xp(10, 20, amount=5, now=100.0)
    xp2 = await service.award_message_xp(10, 20, amount=5, now=110.0)
    xp3 = await service.award_message_xp(10, 20, amount=5, now=131.0)

    assert xp1 == 5
    assert xp2 == 5
    assert xp3 == 10

    await db.close()
