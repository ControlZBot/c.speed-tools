from cspeed_tools.db.repositories.tags_repo import TagsRepository


class TagsService:
    def __init__(self, repo: TagsRepository):
        self.repo = repo

    async def normalize_tag_name(self, name: str) -> str:
        return await self.repo.normalize_name(name)
