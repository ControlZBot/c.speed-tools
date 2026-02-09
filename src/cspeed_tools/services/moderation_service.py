from cspeed_tools.db.repositories.moderation_repo import ModerationRepository


class ModerationService:
    def __init__(self, repo: ModerationRepository):
        self.repo = repo

    async def create_case(
        self,
        guild_id: int,
        actor_id: int,
        target_id: int,
        action: str,
        reason: str,
    ) -> int:
        if not reason.strip():
            raise ValueError("Reason is required")
        return await self.repo.create_case(guild_id, actor_id, target_id, action, reason)
