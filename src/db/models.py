from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db_setup import Base
from .schemas import ModelsChoiceEnum


class DataFrame(Base):
    __tablename__ = "dataframe"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    target = Column(String, default="target", nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    model = relationship("Model", back_populates="dataframe")


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True, index=True)
    dataframe_id = Column(Integer, ForeignKey("dataframe.id"))
    description = Column(String)
    type = Column(Enum(ModelsChoiceEnum), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    dataframe = relationship("DataFrame", back_populates="model")
