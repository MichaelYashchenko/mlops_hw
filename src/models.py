import json
import os
import pickle
from contextlib import contextmanager
from typing import Dict, Generator, Iterable, Optional, Union

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
import dvc.api

from src.db import crud
from src.db.db_setup import SessionLocal
from src.exceptions import IncorrecTargetError

field_name = str
field_values = dict[str, str]

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
REMOTE_STORAGE = "minio"


@contextmanager
def session_scope() -> Generator[SessionLocal, None, None]:
    """Provides a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class DataFrame:
    short_path = os.path.join("dataframes", "{}.json")
    src_path = os.path.join("src", short_path)

    def __init__(self, dataframe_id: int) -> None:
        with session_scope() as db:
            dataframe_inst = crud.get_dataframe(db, dataframe_id)
            db.expunge_all()
        target = dataframe_inst.target

        df = self._load(dataframe_id)
        if target not in df.columns:
            raise IncorrecTargetError(target)

        self._target = df.target
        self._data = df.drop(target, axis=1)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def target(self) -> pd.Series:
        return self._target

    @classmethod
    def delete(cls, dataframe_id: int) -> None:
        os.remove(cls.src_path.format(dataframe_id))

    @classmethod
    def save(
        cls, dataframe_id: int, dataframe_dict: Dict[field_name, field_values]
    ) -> None:
        save_path = cls.src_path.format(dataframe_id)
        with open(save_path, "w") as f:
            json.dump(dataframe_dict, f, indent=4)
        os.system(f"dvc add {save_path}")
        os.system(f"dvc push")

    @classmethod
    def _load(cls, dataframe_id: int) -> pd.DataFrame:
        with dvc.api.open(
            cls.src_path.format(dataframe_id),
            remote=REMOTE_STORAGE,
        ) as f:
            df = pd.read_json(f)
        return df


class Model:
    model_cls = None
    short_path = os.path.join("models", "{}.sav")
    src_path = os.path.join("src", short_path)

    @classmethod
    def fit(
        cls, model_id: int, dataframe_id: int, hyperparams: Optional[dict] = None
    ) -> None:
        dataframe = DataFrame(dataframe_id)
        x_train, y_train = dataframe.data, dataframe.target
        if hyperparams:
            model = cls.model_cls(**hyperparams)
        else:
            model = cls.model_cls()
        model.fit(x_train, y_train)
        cls._save(model_id, model)

    @classmethod
    def predict(
        cls, model_id: int, x_test: Dict[field_name, field_values]
    ) -> Iterable[float]:
        model = cls._load(model_id)
        df_test = pd.DataFrame.from_dict(x_test)
        return model.predict(df_test)

    @classmethod
    def fit_with_validation(
        cls,
        model_id: int,
        dataframe_id: int,
        hyperparams_grid: dict[str, list[Union[str, int, float, bool]]],
    ) -> None:
        model = cls.model_cls()
        dataframe = DataFrame(dataframe_id)
        x_train, y_train = dataframe.data, dataframe.target
        grid_search = GridSearchCV(model, hyperparams_grid)
        grid_search.fit(x_train, y_train)
        cls._save(model_id, grid_search)

    @classmethod
    def delete_model(cls, model_id: int) -> None:
        os.remove(cls.src_path.format(model_id))

    @classmethod
    def _save(cls, model_id: int, model: BaseEstimator) -> None:
        save_path = cls.src_path.format(model_id)
        with open(save_path, "wb") as f:
            pickle.dump(model, f)
        os.system(f"dvc add {save_path}")
        os.system(f"dvc push")

    @classmethod
    def _load(cls, model_id: int) -> BaseEstimator:
        with dvc.api.open(
            cls.src_path.format(model_id),
            mode="rb",
            remote=REMOTE_STORAGE,
        ) as f:
            model = pickle.load(f)
        return model


class LinearModel(Model):
    model_cls = LinearRegression


class TreeModel(Model):
    model_cls = DecisionTreeRegressor
