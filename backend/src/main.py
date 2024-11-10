import logging

from fastapi import FastAPI

from .config import Settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info(f"Settings: {Settings().model_dump()}")


@app.get("/")
def root():
    return


@app.post("/report")
def report():
    return
