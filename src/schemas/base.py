from pydantic import BaseModel


class ShortUrl(BaseModel):
    short_url: str


class ShortUrlWithOrigin(ShortUrl):
    original_url: str


class ShortUrlWithId(ShortUrl):
    short_id: int


class CreateShortUrl(BaseModel):
    original_url: str


class ShortUrlStatic(ShortUrlWithOrigin):
    use: int
