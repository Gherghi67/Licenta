from typing import List

from datetime import datetime

from pydantic import BaseModel


class ReportBase(BaseModel):
    #timestamp: datetime
    has_mask: bool


class ReportCreate(ReportBase):
    pass


class Report(ReportBase):
    id: int
    public_place_id: int

    class Config:
        orm_mode = True


class PublicPlaceBase(BaseModel):
    name: str
    owner: str


class PublicPlaceCreate(PublicPlaceBase):
    pass


class PublicPlace(PublicPlaceBase):
    id: int
    reports: List[Report] = []

    class Config:
        orm_mode = True
