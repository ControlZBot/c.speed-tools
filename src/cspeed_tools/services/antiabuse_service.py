class AntiabuseService:
    def is_safe_mention_count(self, mention_count: int, threshold: int = 10) -> bool:
        return mention_count <= threshold
