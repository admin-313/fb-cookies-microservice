from pydantic import BaseModel, ConfigDict


class FacebookToken(BaseModel):
    model_config = ConfigDict(strict=True)

    token: str
    cookie: str


class JSONFBWebdriverConfig(BaseModel):
    model_config = ConfigDict(strict=True)

    proxy: str
    user_agent: str
    cookie: str
