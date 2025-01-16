import uvicorn
import logging
from fastapi import FastAPI
from facebook.router import router


logging.basicConfig(level=10)

app = FastAPI()
logging.info("The app has been started")
app.include_router(router=router)
logging.info("The routers have been attached")

# This two lines of code were made for debug to work properly with FastAPI
# docs: https://fastapi.tiangolo.com/tutorial/debugging/
if __name__ == "__main__":
    logging.debug("Uvicorn runs in DEBUG mode!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
