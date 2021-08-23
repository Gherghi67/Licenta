from typing import List

from datetime import datetime

from pydantic import BaseModel


class ReportBase(BaseModel):
    pass


class ReportCreate(ReportBase):
    pass


class Report(ReportBase):
    id: int
    public_place_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class PublicPlaceBase(BaseModel):
    name: str
    owner: str
    address: str
    max_capacity: int


class PublicPlaceCreate(PublicPlaceBase):
    pass


class PublicPlace(PublicPlaceBase):
    id: int
    reports: List[Report] = []

    class Config:
        orm_mode = True


class Response(BaseModel):
    has_mask: bool
