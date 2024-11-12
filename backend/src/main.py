import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session

from .config import get_settings
from .postgis import create_db_and_tables, get_session

settings = get_settings()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On app startup, create tables
    create_db_and_tables()
    yield


@app.get("/")
def root():
    return


@app.post("/report")
def report():
    return
