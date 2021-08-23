from sqlalchemy.orm import Session

import models
import schemas
import datetime

from check_mask import check_mask


def get_public_place(db: Session, public_place_id: int):
    public_place = db.query(models.PublicPlace).filter(
        models.PublicPlace.id == public_place_id).first()

    return public_place


def get_public_places(db: Session):
    public_places = db.query(models.PublicPlace).all()

    return public_places


def create_public_place(db: Session, public_place: schemas.PublicPlaceCreate):
    db_public_place = models.PublicPlace(
        name=public_place.name, owner=public_place.owner, address=public_place.address, max_capacity=public_place.max_capacity)

    db.add(db_public_place)
    db.commit()
    db.refresh(db_public_place)

    return db_public_place


async def create_report(db: Session, public_place_id: int, file, model):
    has_mask = await check_mask(model=model, file=file)

    if (has_mask == False):
        db_report = models.Report(
            public_place_id=public_place_id,
            timestamp=datetime.datetime.now())

        db.add(db_report)
        db.commit()
        db.refresh(db_report)

        return schemas.Response(has_mask=False)

    return schemas.Response(has_mask=True)


def delete_report(db: Session, report_id: int):
    report = db.query(models.Report).filter(
        models.Report.id == report_id).first()

    db.delete(report)
    db.commit()

    return report
