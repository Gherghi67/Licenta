from typing import List
from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/public-places/', response_model=List[schemas.PublicPlace])
def get_public_places(db: Session = Depends(get_db)):
    public_places = crud.get_public_places(db=db)
    print(public_places)
    return {"public_places": public_places}


@app.get('/public-places/{public_place_id}', response_model=schemas.PublicPlace)
def get_public_place(public_place_id: int, db: Session = Depends(get_db)):
    db_public_place = crud.get_public_place(
        db=db, public_place_id=public_place_id)
    return db_public_place


@app.post('/public-places/', response_model=schemas.PublicPlace)
def create_public_place(public_place: schemas.PublicPlaceCreate, db: Session = Depends(get_db)):
    return crud.create_public_place(db=db, public_place=public_place)
