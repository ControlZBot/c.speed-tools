class IntegrationsService:
    def normalize_webhook_name(self, name: str) -> str:
        return name.strip()[:80]
