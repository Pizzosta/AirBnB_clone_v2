#!/usr/bin/python3
"""Define Place class for Airbnb console"""
from sqlalchemy.ext.declarative import declarative_base
from models import storage_type
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity


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
    if storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            ''' returns list of review instances with place_id
                equals to the cyrrent Place.id
                FileStorage relationship between Place and Review
            '''
            from models import storage
            all_revs = storage.all(Review)
            lst = []
            for rev in all_revs.values():
                if rev.place_id == self.id:
                    lst.append(rev)
            return lst

        @property
        def amenities(self):
            ''' returns the list of Amenity instances
                based on the attribute amenity_ids that
                contains all Amenity.id linked to the Place
            '''
            from models import storage
            all_amens = storage.all(Amenity)
            lst = []
            for amen in all_amens.values():
                if amen.id in self.amenity_ids:
                    lst.append(amen)
            return lst

        @amenities.setter
        def amenities(self, obj):
            ''' method for adding an Amenity.id to the
                attribute amenity_ids. accepts only Amenity
                objects
            '''
            if obj is not None:
                if isinstance(obj, Amenity):
                    if obj.id not in self.amenity_ids:
                        self.amenity_ids.append(obj.id)
     
