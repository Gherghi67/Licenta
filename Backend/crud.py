from sqlalchemy.orm import Session

import models
import schemas


def get_public_place(db: Session, public_place_id: int):
    query = db.query(models.PublicPlace).filter(
        models.PublicPlace.id == public_place_id).first()

    return db.execute(query)


def get_public_places(db: Session):
    query = db.query(models.PublicPlace).all()

    public_places = db.execute(query)

    print(public_places)

    return public_places


def create_public_place(db: Session, public_place: schemas.PublicPlaceCreate):
    db_public_place = models.PublicPlace(
        name=public_place.name, owner=public_place.owner)

    db.add(db_public_place)
    db.commit()
    db.refresh(db_public_place)

    return db_public_place
