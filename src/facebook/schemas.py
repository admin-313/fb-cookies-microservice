from pydantic import BaseModel, ConfigDict


class JSONFBWebdriverConfig(BaseModel):
    model_config = ConfigDict(strict=True)

    proxy: str
    user_agent: str
    cookie: str
    adsmanager_link: str


class ParserResponce(BaseModel):
    model_config = ConfigDict(strict=True)

    cookie: str
    access_token: str
