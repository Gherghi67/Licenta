from typing import List
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

from tensorflow.keras.models import load_model

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])

model = load_model('../Clasificatoare/Clasificator_Wild')


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@ app.get('/')
def hello_world():
    return{'hello': 'world'}


@ app.get('/public-places/', response_model=List[schemas.PublicPlace])
def get_public_places(db: Session = Depends(get_db)):
    public_places = crud.get_public_places(db=db)
    return public_places


@ app.get('/public-places/{public_place_id}', response_model=schemas.PublicPlace)
def get_public_place(public_place_id: int, db: Session = Depends(get_db)):
    db_public_place = crud.get_public_place(
        db=db, public_place_id=public_place_id)
    return db_public_place


@ app.post('/public-places/', response_model=schemas.PublicPlace)
def create_public_place(public_place: schemas.PublicPlaceCreate, db: Session = Depends(get_db)):
    return crud.create_public_place(db=db, public_place=public_place)


@ app.post('/public-places/{public_place_id}/reports', response_model=schemas.Response)
async def create_report(public_place_id: int, db: Session = Depends(get_db),
                        file: UploadFile = File(...)):
    print(public_place_id)
    return await crud.create_report(db=db, public_place_id=public_place_id,
                                    file=file, model=model)


@ app.delete('/public-places/reports/{report_id}/', response_model=schemas.Report)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return crud.delete_report(db=db, report_id=report_id)
