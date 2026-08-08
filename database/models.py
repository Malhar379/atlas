from core.execution.status import RunStatus
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


from database.base import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    plugin = Column(String(100), nullable=False)

    runs = relationship(
        "Run",
        back_populates="experiment",
        cascade="all, delete-orphan"
    )


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True)

    experiment_id = Column(
        Integer,
        ForeignKey("experiments.id"),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default=RunStatus.CREATED.value
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    experiment = relationship(
        "Experiment",
        back_populates="runs"
    )