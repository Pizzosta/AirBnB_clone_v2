#!/usr/bin/python3
"""Creates DB storage engine for AirBnB clone objects"""

from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """create sqlalchemy storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """initialize/create engine"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        db_host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password,
                                              db_host, db_name),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Queries db session for all objects depending on the class name
        Returns a dict
        """
        result = {}
        mod_args = [User, State, City, Amenity, Place, Review]
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                result[key] = obj
        else:
            for clas in mod_args:
                objs = self.__session.query(clas).all()
                for obj in objs:
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    result[key] = obj
        return result

    def new(self, obj):
        """Add object to current db session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """Commit all changes in current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current db session if not none"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        """creates all tables in the db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """closes the working SQLAlchemy session"""
        self.__session.remove()
