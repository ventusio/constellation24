# Create database URL
from datetime import datetime, timezone
from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import URL
from sqlmodel import Column, Field, Session, SQLModel, create_engine
from src.models import Point, Report

from .config import get_settings

settings = get_settings()

# Setup database
database_url = URL.create(
    drivername="postgresql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)
engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class DbReports(SQLModel, table=True):
    __tablename__ = "reports"

    model_config = {"arbitrary_types_allowed": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    geom: Geometry = Field(sa_column=Column(Geometry("Point", srid=4326)))
    timestamp: Optional[datetime] = Field(default=datetime.now(timezone.utc))

    def as_report(self) -> Report:
        return Report(id=self.id, location=Point.from_geom(self.geom), timestamp=self.timestamp.isoformat())

    def from_report(report: Report):
        return DbReports(id=report.id, geom=report.location.as_geom(), timestamp=report.timestamp)
