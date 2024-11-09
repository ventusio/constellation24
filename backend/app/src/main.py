import logging

from fastapi import FastAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def root():
    logger.info("Hello World")
    return {"Hello": "World"}
