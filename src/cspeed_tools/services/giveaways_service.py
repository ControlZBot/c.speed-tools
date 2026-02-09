class GiveawaysService:
    def validate_duration_minutes(self, minutes: int) -> int:
        if minutes <= 0:
            raise ValueError("Duration must be positive")
        return minutes
