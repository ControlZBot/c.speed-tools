import pytest
from cspeed_tools.checks import owner_only

class DummyUser:
    def __init__(self, user_id: int):
        self.id = user_id

class DummyInteraction:
    def __init__(self, user_id: int):
        self.user = DummyUser(user_id)

@pytest.mark.asyncio
async def test_owner_check_passes() -> None:
    async def handler() -> None:
        return None
    wrapped = owner_only(10)(handler)
    checks = getattr(wrapped, "__discord_app_commands_checks__")
    assert await checks[0](DummyInteraction(10))
