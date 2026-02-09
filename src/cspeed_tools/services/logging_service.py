class LoggingService:
    def format_staff_action(self, action: str, reason: str) -> str:
        safe_reason = reason.strip() or "No reason provided"
        return f"c.speed-tools | {action} | {safe_reason}"
