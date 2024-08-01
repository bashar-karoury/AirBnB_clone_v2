#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import os
storage_env = os.environ.get('HBNB_TYPE_STORAGE')

if storage_env == 'db':
    from models.base_model import Base

    class State(BaseModel, Base):
        """ State class """
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete", backref="state")
else:
    class State(BaseModel):
        """ State class """
        name = ''

        @property
        def cities(self):
            """ Getter attribute for retrieving all cities of this State
            in FileStorage
            """
            # File Storage
            from models import storage
            cities_dict = storage.all(City)
            # filter in associated cities with current id
            res = [v for k, v in cities_dict.items() if v.state_id == self.id]
            return res
