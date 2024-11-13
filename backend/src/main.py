import logging
from contextlib import asynccontextmanager
from typing import Annotated, List

import numpy as np
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlmodel import Session, delete, select
from src.config import Settings, get_settings
from src.postgis import DbReports, create_db_and_tables, get_session

# isort: off
# these need to be imported in a certain order
from .utils import add_root_to_path  # noqa isort:skip
from shared.models import Point, Report


settings = get_settings()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SessionDep = Annotated[Session, Depends(get_session)]
api_key_header = APIKeyHeader(name="X-Admin-Key")


def validate_api_key(
    api_key: Annotated[str, Security(api_key_header)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    if api_key != settings.admin_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


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


@app.delete("/admin/reports")
def delete_all_reports(
    session: SessionDep,
    api_key: str = Security(validate_api_key),
) -> dict:
    deleted_count = session.exec(delete(DbReports)).rowcount
    session.commit()
    return {"message": f"Deleted {deleted_count} reports"}


@app.post("/admin/reports")
def create_mock_reports(
    location: Point,
    amount: int,
    session: SessionDep,
    api_key: str = Security(validate_api_key),
) -> List[Report]:
    points = np.random.normal(size=(amount, 2)) * np.array([[0.05, 0.05]]) + np.array([[location.lat, location.lng]])
    db_reports = [DbReports(geom=Point(lat=point[0], lng=point[1]).as_geom()) for point in points]
    session.add_all(db_reports)
    session.commit()
    return [db_report.as_report() for db_report in db_reports]
