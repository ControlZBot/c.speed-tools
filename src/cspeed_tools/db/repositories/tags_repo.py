from . import BaseRepository


class TagsRepository(BaseRepository):
    async def normalize_name(self, name: str) -> str:
        return name.strip().lower()
