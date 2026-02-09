from . import BaseRepository


class RemindersRepository(BaseRepository):
    async def validate_reminder(self, content: str) -> bool:
        return bool(content.strip())
