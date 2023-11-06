from typing import Optional
from enum import Enum

from pydantic import BaseModel


class ModelsChoice(str, Enum):
    Linear = 'linear'
    Tree = 'tree'


class ItemBase(BaseModel):
    id: int
    description: Optional[str] = None


class DataFrame(ItemBase):
    class Config:
        orm_mode = True


class Model(ItemBase):
    type: ModelsChoice

    class Config:
        orm_mode = True
