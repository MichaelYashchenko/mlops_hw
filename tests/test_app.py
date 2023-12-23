import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.db.db_setup import Base
from src.db import schemas
from src.api.main import app, get_db, DataFrame, LinearModel, Model

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_dataframe(monkeypatch, empty_call) -> None:
    monkeypatch.setattr(DataFrame, "save", value=empty_call)
    response = client.post(
        "/dataframes/",
        json={
            "dataframe": schemas.DataFrameCreate(
                description="gachi dataset",
                target="target",
            ).model_dump(),
            "dataframe_dict": {},
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["description"] == "gachi dataset"
    assert data["id"] == 1
    assert data["target"] == "target"


def test_read_dataframes() -> None:
    response = client.get(
        "/dataframes/",
        params={"skip": 0, "limit": 100},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    dataframe_info = data[0]
    assert dataframe_info["description"] == "gachi dataset"
    assert dataframe_info["id"] == 1
    assert dataframe_info["target"] == "target"


def test_read_dataframe() -> None:
    dataframe_id = 1
    response = client.get(f"/dataframes/{dataframe_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["description"] == "gachi dataset"
    assert data["id"] == dataframe_id
    assert data["target"] == "target"


def test_read_dataframe_with_exception() -> None:
    dataframe_id = 2  # Does not exist
    response = client.get(f"/dataframes/{dataframe_id}/")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "DataFrame not found"


def test_create_model(monkeypatch, empty_call) -> None:
    monkeypatch.setattr(LinearModel, "fit", value=empty_call)
    response = client.post(
        "/models/",
        json={
            "model": schemas.ModelCreate(
                dataframe_id=1,
                description="gachi model",
                type="Linear",
            ).model_dump(),
            "hyperparams": {},
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["dataframe_id"] == 1
    assert data["description"] == "gachi model"
    assert data["id"] == 1
    assert data["type"] == "Linear"


def test_create_model_with_validation(monkeypatch, empty_call) -> None:
    monkeypatch.setattr(LinearModel, "fit_with_validation", value=empty_call)
    response = client.post(
        "/models/validation/",
        json={
            "model": schemas.ModelCreate(
                dataframe_id=1,
                description="gachi model",
                type="Linear",
            ).model_dump(),
            "hyperparams_grid": {},
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["dataframe_id"] == 1
    assert data["description"] == "gachi model"
    assert data["id"] == 2
    assert data["type"] == "Linear"


def test_read_models() -> None:
    response = client.get(
        "/models/",
        params={"skip": 0, "limit": 100},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2


def test_read_model() -> None:
    model_id = 1
    response = client.get(f"/models/{model_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["dataframe_id"] == 1
    assert data["description"] == "gachi model"
    assert data["id"] == model_id
    assert data["type"] == "Linear"


def test_read_model_with_exception() -> None:
    model_id = 3  # Does not exist
    response = client.get(f"/models/{model_id}/")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Model not found"


def test_models_predict(monkeypatch) -> None:
    y_pred = [0, 1, 1, 1, 0]

    def _predict(*args, **kwargs):
        return y_pred

    monkeypatch.setattr(Model, "predict", value=_predict)
    response = client.post(
        "/models/predict/",
        json={
            "mdl_info": schemas.Predict(model_id=1).model_dump(),
            "dataframe": {}
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["result"] == y_pred


def test_delete_model(monkeypatch, empty_call) -> None:
    monkeypatch.setattr(os, "remove", value=empty_call)
    model_id = 1
    response = client.delete(f"/models/{model_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Model deleted"


def test_delete_dataframe(monkeypatch, empty_call) -> None:
    monkeypatch.setattr(os, "remove", value=empty_call)
    dataframe_id = 1
    response = client.delete(f"/dataframes/{dataframe_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Dataframe deleted"


def test_read_available_models() -> None:
    response = client.get("/models/available/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["models"] == ["Linear", "Tree"]
