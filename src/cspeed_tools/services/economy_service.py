from cspeed_tools.db.repositories.economy_repo import EconomyRepository


class EconomyService:
    def __init__(self, repo: EconomyRepository):
        self.repo = repo

    async def normalize_amount(self, amount: int) -> int:
        return await self.repo.sanitize_amount(amount)
