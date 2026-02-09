from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from cspeed_tools.bot import CSpeedBot, ServiceContainer


class DummyRepo:
    async def is_globally_banned(self, user_id: int) -> bool:
        return False


class DummyGlobalService:
    def __init__(self) -> None:
        self.repo = DummyRepo()


@pytest.mark.asyncio
async def test_command_tree_matches_manifest() -> None:
    settings = SimpleNamespace(dev_guild_id=None, owner_user_id=1275585606688444438)
    container = ServiceContainer(settings=settings, db=None, global_actions_service=DummyGlobalService())
    bot = CSpeedBot(container)
    await bot.load_extension("cspeed_tools.cogs.core_cog")
    await bot.load_extension("cspeed_tools.cogs.owner_cog")
    await bot.load_extension("cspeed_tools.cogs.misc_cog")

    manifest = yaml.safe_load(
        Path("src/cspeed_tools/manifest/commands_manifest.yaml").read_text(encoding="utf-8")
    )["endpoints"]

    def flatten(commands, prefix=""):
        paths = set()
        for command in commands:
            current = f"{prefix}/{command.name}"
            if hasattr(command, "commands"):
                paths |= flatten(command.commands, current)
            else:
                paths.add(current)
        return paths

    tree_paths = flatten(bot.tree.get_commands(guild=None))
    manifest_paths = {str(entry["path"]) for entry in manifest}

    assert tree_paths == manifest_paths
    assert all(not __import__("re").search(r"/group\d+|/cmd\d+$", path) for path in tree_paths)
    assert all("cmd group" not in path for path in tree_paths)

    await bot.close()
