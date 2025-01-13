from fastapi import APIRouter
from facebook.services.geckodriver.geckodriver_web_driver_impl import GeckodriverFBWebDriverImpl

router = APIRouter()

@router.get("/parse")
async def read_parse() -> str:
    driver = GeckodriverFBWebDriverImpl()
    await driver.run_facebook_parser()
    return ""