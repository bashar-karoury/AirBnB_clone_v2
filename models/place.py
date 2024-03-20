#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    name = Column(String(128), nullable=False)
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    reviews = relationship("Review", cascade="all, delete", backref="place")
    # amenity_ids = []

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
            reviews_list = [v for k, v in rev_dict if v.review_id == self.id]
            return reviews_list
