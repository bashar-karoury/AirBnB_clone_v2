#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, City
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    @property
    def cities(self):
        """ Getter attribute for retrieving all cities of this State
        in FileStorage
        """
        # Get type of storage
        storage_env = os.environ.get('HBNB_TYPE_STORAGE')

        if storage_env == 'db':
            return self.cities
        else:
            # File Storage
            from models import storage
            cities_dict = all(self, City)
            # filter in associated cities with current id
            cities_list = [v for k, v in cities_dict if v.state_id == self.id]
            return cities_list
