from pydantic import BaseModel, field_validator


class ChatMessage(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Message is empty')
        if len(v) > 200:
            raise ValueError('Message is too long (max 200 characters)')
        return v