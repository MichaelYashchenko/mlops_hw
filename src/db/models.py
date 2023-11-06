import enum
from sqlalchemy import Column, Integer, String, Enum

from .db_setup import Base


class ModelsChoiceEnum(enum.Enum):
    Linear = 'linear'
    Tree = 'tree'


class DataFrame(Base):
    __tablename__ = "dataframe"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    type = Column(Enum(ModelsChoiceEnum), nullable=False)
