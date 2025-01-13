from fastapi import APIRouter
from facebook.services.geckodriver.geckodriver_web_driver_impl import GeckodriverFBWebDriverImpl

router = APIRouter()
driver = GeckodriverFBWebDriverImpl()

@router.get("/parse")
async def read_parse() -> str:
    await driver.run_facebook_parser()
    return ""