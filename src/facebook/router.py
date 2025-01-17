import logging
from fastapi import APIRouter, HTTPException
from facebook.schemas import ParserResponce
from facebook.services.geckodriver.geckodriver_web_driver_impl import (
    GeckodriverFBWebDriverImpl,
)
from facebook.exceptions import (
    FBDriverJSParseException,
    Socks5ProxyParseFail,
    FBWebdriverCouldNotLoginToFb,
    FBWebdriverHasNotBeenInstanciated,
    FBWebdriverInvalidConfigProvided,
)


router = APIRouter()


@router.get("/parse")
async def read_parse():
    driver = GeckodriverFBWebDriverImpl()
    try:
        responce: ParserResponce = await driver.run_facebook_parser()
        return responce.model_dump()
    
    except FBDriverJSParseException as js_ex:
        logging.error(str(js_ex))

        raise HTTPException(
            status_code=500,
            detail="Failed to parse the data from the obtained facebook page :c",
        )

    except Socks5ProxyParseFail as s5ppf:
        logging.error(f"Failed to get SOCKS5 proxy {str(s5ppf)}")

        raise HTTPException(
            status_code=500, detail="We couldn't parse the proxy for webdriver config"
        )

    except FBWebdriverCouldNotLoginToFb as fbwcnlf:
        logging.error(f"Webdriver failed to login to Facebook {str(fbwcnlf)}")

        raise HTTPException(status_code=500, detail="Webdriver Error")

    except FBWebdriverInvalidConfigProvided as conf_err:
        logging.error(f"Bad user config: {str(conf_err)}")

        raise HTTPException(status_code=500, detail="Wrong config provided")

    except FBWebdriverHasNotBeenInstanciated as e:
        logging.critical(f"Internal webdriver issue {str(e)}")

        raise HTTPException(status_code=500, detail="Webdriver Error")

    except Exception as e:
        logging.critical(f"Unexpected error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Unexpected error. Things were never meant to go this way",
        )
    finally:
        logging.info("The /parse thread terminated")
