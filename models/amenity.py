#!/usr/bin/python3
"""Defines Amnity class for AirBnB clone"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Define place amenities in an AirBnB

    Attr:
        name(str): name of amenity
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
