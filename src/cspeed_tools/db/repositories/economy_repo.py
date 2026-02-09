from . import BaseRepository


class EconomyRepository(BaseRepository):
    async def sanitize_amount(self, amount: int) -> int:
        return max(0, int(amount))
