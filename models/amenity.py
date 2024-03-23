#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
# from models.place import Place
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import os
storage_env = os.environ.get('HBNB_TYPE_STORAGE')

if storage_env == 'db':
    from models.place import place_amenity

    class Amenity(BaseModel, Base):
        """ Class to represent amenity of place
        """
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            "Place",
            secondary=place_amenity,
            # backref="amenities",
            viewonly=True)
else:
    class Amenity(BaseModel):
        """ Class to represent amenity of place
        """
        name = ""
