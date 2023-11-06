from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.db import crud, schemas
from src.db.db_setup import SessionLocal
from src.models import DataFrame, LinearModel, Model, TreeModel

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dataframes/", response_model=schemas.DataFrame, tags=["Dataframes"])
def create_dataframe(
    dataframe: schemas.DataFrameCreate,
    dataframe_dict: Optional[dict] = None,
    db: Session = Depends(get_db),
):
    db_dataframe = crud.create_dataframe(db=db, dataframe=dataframe)
    DataFrame.save(db_dataframe.id, dataframe_dict)
    return db_dataframe


@app.get("/dataframes/", response_model=list[schemas.DataFrame], tags=["Dataframes"])
def read_dataframes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_dataframes(db=db, skip=skip, limit=limit)


@app.get(
    "/dataframes/{dataframe_id}/", response_model=schemas.DataFrame, tags=["Dataframes"]
)
def read_dataframe(dataframe_id: int, db: Session = Depends(get_db)):
    db_dataframe = crud.get_dataframe(db=db, dataframe_id=dataframe_id)
    if db_dataframe is None:
        raise HTTPException(status_code=404, detail="DataFrame not found")
    return db_dataframe


@app.delete("/dataframes/{dataframe_id}/", tags=["Dataframes"])
def delete_dataframe(dataframe_id: int, db: Session = Depends(get_db)):
    crud.delete_dataframe(db=db, dataframe_id=dataframe_id)
    DataFrame.delete(dataframe_id)
    return {"message": "Dataframe deleted"}


@app.post("/models/", response_model=schemas.Model, tags=["Models"])
def create_model(
    model: schemas.ModelCreate,
    hyperparams: Optional[dict] = None,
    db: Session = Depends(get_db),
):
    db_model = crud.create_model(db=db, model=model)
    model_learner = LinearModel
    if db_model.type == schemas.ModelsChoiceEnum.Tree:
        model_learner = TreeModel
    model_learner.fit(db_model.id, db_model.dataframe_id, hyperparams)
    return db_model


@app.post("/models/validation/", response_model=schemas.Model, tags=["Models"])
def create_model_with_validation(
    model: schemas.ModelCreate,
    hyperparams_grid: dict = None,
    db: Session = Depends(get_db),
):
    db_model = crud.create_model(db=db, model=model)
    model_learner = LinearModel
    if db_model.type == schemas.ModelsChoiceEnum.Tree:
        model_learner = TreeModel
    model_learner.fit_with_validation(
        db_model.id, db_model.dataframe_id, hyperparams_grid
    )
    return db_model


@app.get("/models/", response_model=list[schemas.Model], tags=["Models"])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_models(db=db, skip=skip, limit=limit)


@app.get("/models/available/", response_model=schemas.ModelsAvailable, tags=["Models"])
def read_available_models():
    return schemas.ModelsAvailable()


@app.post("/models/predict/", response_model=schemas.PredictResult, tags=["Models"])
def predict(
    model_info: schemas.Predict, dataframe: dict, db: Session = Depends(get_db)
):
    db_model = crud.get_model(db=db, model_id=model_info.model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    result = Model.predict(model_info.model_id, dataframe)
    return schemas.PredictResult(result=result)


@app.get("/models/{model_id}/", response_model=schemas.Model, tags=["Models"])
def read_model(model_id: int, db: Session = Depends(get_db)):
    db_model = crud.get_model(db=db, model_id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_model


@app.delete("/models/{model_id}/", tags=["Models"])
def delete_model(model_id: int, db: Session = Depends(get_db)):
    Model.delete_model(model_id)
    crud.delete_model(db=db, model_id=model_id)
    return {"message": "Model deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
