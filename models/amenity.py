#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
# from models.place import Place
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.place import place_amenity
import os
storage_env = os.environ.get('HBNB_TYPE_STORAGE')

class Amenity(BaseModel, Base):
    if storage_env == 'db':    
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            "Place",
            secondary=place_amenity,
            # backref="amenities",
            viewonly=True)
    else:
        name = ""