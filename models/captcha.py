from pydantic import BaseModel


class Captcha(BaseModel):
    url: str
    text: str = None
