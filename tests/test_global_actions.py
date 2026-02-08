import pytest
from cspeed_tools.db.engine import Database
from cspeed_tools.db.migrations import run_migrations
from cspeed_tools.db.repositories.global_actions_repo import GlobalActionsRepository

@pytest.mark.asyncio
async def test_global_ban_roundtrip(tmp_path) -> None:
    db = Database(f"sqlite+aiosqlite:///{tmp_path}/x.db")
    await db.connect()
    await run_migrations(db)
    repo = GlobalActionsRepository(db)
    await repo.add_global_ban(123, "r", 999)
    assert await repo.is_globally_banned(123)
    await repo.remove_global_ban(123)
    assert not await repo.is_globally_banned(123)
    await db.close()
