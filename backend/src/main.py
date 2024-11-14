import logging
from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from .config import get_settings
from .postgis import DbReports, create_db_and_tables, get_session

# isort: off
# these need to be imported in a certain order
from .utils import add_root_to_path  # noqa

from shared.models import Point, Report


settings = get_settings()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On app startup, create tables
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return


@app.post("/report")
def create_report(location: Point, session: SessionDep) -> Report:
    db_report = DbReports(geom=location.as_geom())
    session.add(db_report)
    session.commit()
    session.refresh(db_report)

    return db_report.as_report()


@app.get("/report/{id}")
def get_report(id: int, session: SessionDep) -> Report:
    report = session.exec(select(DbReports).where(DbReports.id == id)).first()
    return report.as_report()


@app.get("/reports")
def get_all_reports(session: SessionDep) -> List[Report]:
    reports = session.exec(select(DbReports)).all()
    return [report.as_report() for report in reports]
