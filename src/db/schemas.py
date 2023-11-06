import enum
from datetime import datetime
from typing import Iterable, Optional

from pydantic import BaseModel


class ModelsChoiceEnum(str, enum.Enum):
    Linear = "Linear"
    Tree = "Tree"


class DataFrameCreate(BaseModel):
    description: Optional[str] = None
    target: str = "target"


class DataFrame(DataFrameCreate):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True


class ModelCreate(BaseModel):
    dataframe_id: int
    description: Optional[str] = None
    type: ModelsChoiceEnum

    class Config:
        use_enum_values = True


class Model(ModelCreate):
    id: int
    created_date: datetime

    class Config:
        use_enum_values = True
        orm_mode = True


class ModelsAvailable(BaseModel):
    models: list[str] = [m.value for m in ModelsChoiceEnum]


class Predict(BaseModel):
    model_id: int


class PredictResult(BaseModel):
    result: Iterable[float]
