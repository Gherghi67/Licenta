from sqlalchemy.orm import relationship
from database import Base

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class PublicPlace(Base):
    __tablename__ = 'public_place'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner = Column(String)

    reports = relationship('Report', back_populates='public_place')


class Report(Base):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True, index=True)
    #timestamp = Column(DateTime)
    has_mask = Column(Boolean)

    public_place_id = Column(Integer, ForeignKey('public_place.id'))

    public_place = relationship('PublicPlace', back_populates='reports')
