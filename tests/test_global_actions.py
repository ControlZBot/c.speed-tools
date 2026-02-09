import pytest

from cspeed_tools.db.engine import Database
from cspeed_tools.db.migrations import run_migrations
from cspeed_tools.db.repositories.global_actions_repo import GlobalActionsRepository
from cspeed_tools.services.global_actions_service import GlobalActionsService


class DummyMember:
    def __init__(self, user_id: int):
        self.id = user_id
        self.banned = False

    async def ban(self, reason: str) -> None:
        self.banned = "global ban enforcement" in reason


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


@pytest.mark.asyncio
async def test_global_ban_join_enforcement(tmp_path) -> None:
    db = Database(f"sqlite+aiosqlite:///{tmp_path}/y.db")
    await db.connect()
    await run_migrations(db)
    repo = GlobalActionsRepository(db)
    service = GlobalActionsService(repo)

    await repo.add_global_ban(444, "reason", 1)
    member = DummyMember(444)
    enforced = await service.enforce_on_join(member)
    assert enforced
    assert member.banned

    member_not_banned = DummyMember(445)
    not_enforced = await service.enforce_on_join(member_not_banned)
    assert not not_enforced
    assert not member_not_banned.banned

    await db.close()
