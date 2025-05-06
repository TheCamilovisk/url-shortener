from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


class ShortenRequestSchema(BaseModel):
    url: str


class ShortenResponseSchema(BaseModel):
    short_url: str
    original_url: str
