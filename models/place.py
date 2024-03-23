#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

import os
storage_env = os.environ.get('HBNB_TYPE_STORAGE')

place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60),  ForeignKey('places.id'), nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), nullable=False)
    )


class Place(BaseModel, Base):
    """ A place to stay """
    if storage_env == 'db':    
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship("Review", cascade="all, delete", backref="place")
        amenities   = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False
            )
        
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
        """ Getter attribute for retrieving all reviews of this Place
        in FileStorage
        """
        # Get type of storage
        storage_env = os.environ.get('HBNB_TYPE_STORAGE')

        if storage_env == 'db':
            return self.reviews
        else:
            # File Storage
            from models import storage
            rev_dict = all(self, Review)
            # filter in associated reviews with current id
            reviews_list = [v for k, v in rev_dict if v.place_id == self.id]
            return reviews_list

    if storage_env != 'db':
        @property
        def amenities(self):
            # File Storage
            amen_dict = all(self, Amenity)
            # filter in associated reviews with current id
            amenities_list = [v for k, v in amen_dict if v.place_id == self.id]
            return amenities_list
        @amenities.setter
        def amenities(self, amen):
            # Add ammenity to list of amenity_ids
            if type(amen) == Amenity:
                self.amenity_ids.append(amen.id)
