from sqlalchemy.orm import Session

from . import models, schemas


def get_dataframe(db: Session, dataframe_id: int):
    return (
        db.query(models.DataFrame).filter(models.DataFrame.id == dataframe_id).first()
    )


def get_dataframes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DataFrame).offset(skip).limit(limit).all()


def delete_dataframe(db: Session, dataframe_id: int):
    db.query(models.DataFrame).filter(models.DataFrame.id == dataframe_id).delete()
    db.commit()


def create_dataframe(db: Session, dataframe: schemas.DataFrameCreate):
    db_dataframe = models.DataFrame(**dataframe.model_dump())
    db.add(db_dataframe)
    db.commit()
    db.refresh(db_dataframe)
    return db_dataframe


def get_model(db: Session, model_id: int):
    return db.query(models.Model).filter(models.Model.id == model_id).first()


def get_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Model).offset(skip).limit(limit).all()


def delete_model(db: Session, model_id: int):
    db.query(models.Model).filter(models.Model.id == model_id).delete()
    db.commit()


def create_model(db: Session, model: schemas.ModelCreate):
    db_model = models.Model(**model.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model
