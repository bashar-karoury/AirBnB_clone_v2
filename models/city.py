#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from models.place import Place
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

if storage_env == 'db':
    class City(BaseModel, Base):
        """ The city class, contains state ID and name """
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(128), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", cascade="all, delete", backref="city")
else:
    class City(BaseModel):
        """ The city class, contains state ID and name """
        state_id = ""
        name = ""
