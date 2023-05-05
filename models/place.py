#!/usr/bin/python3
"""This is the place class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Table, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review
from os import getenv
import models


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place.id', String(60),
                             ForeignKey('places.id'), primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """defines place attributes for user

    city_id(str): id of city where place is located
    user_id(str): id of user
    name (str): name of place
    description(str): brief description of place
    number_rooms(int): number of rooms in place
    number_bathrooms(int): number of bathrooms in place
    max_guest(int): maximum number of guests place can accommodate
    price_by_night(int): unit price of place per night
    latitude(float): GPS coordinates of place
    longitude(float): GPS coordinates of place
    amenity_ids(list): list of all amenity ids generated
    """

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    env = getenv('HBNB_TYPE_STORAGE')

    if env == 'db':
        reviews = relationship('Review', cascade='all, delete, delete-orphan',
                               backref='place')
    else:
        @property
        def reviews(self):
            """ Returns list of reviews.id """
            mod_args = model.storage.all()
            mod_args_list = [mod_args[key] for key in mod_args.keys() if
                             isinstance(mod_args[key], Review) and
                             mod_args[key].place_id == self.id and
                             key.replace(".", " ").split[0] == 'Review']
            return mod_args_list

        @property
        def amenities(self):
            """returns list of all amenity ids"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """append method for adding amenity.id to amenity_ids"""
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
