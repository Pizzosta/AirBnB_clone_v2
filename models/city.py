#!/usr/bin/python3
""" City Module for AirBnB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel):
    """Define City class

    Args:
        __tablename__: db object class is linked to
        state_id(str): id of state, city belongs to
        name(str): name of city
    """
    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
    places = relationship('Place', cascade='all, delete, delete-orphan',
                          backref='cities')
