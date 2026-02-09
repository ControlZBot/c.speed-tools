from cspeed_tools.db.repositories.reminders_repo import RemindersRepository


class RemindersService:
    def __init__(self, repo: RemindersRepository):
        self.repo = repo

    async def validate(self, content: str) -> bool:
        return await self.repo.validate_reminder(content)
