class PollsService:
    def sanitize_question(self, question: str) -> str:
        clean = question.strip()
        if not clean:
            raise ValueError("Question is required")
        return clean
