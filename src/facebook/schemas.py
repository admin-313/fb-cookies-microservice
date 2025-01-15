from pydantic import BaseModel, ConfigDict


class FacebookToken(BaseModel):
    model_config = ConfigDict(strict=True)

    token: str
    cookie: str