#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
# from models.place import Place
# from models.user import User
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import os
storage_env = os.environ.get('HBNB_TYPE_STORAGE')

if storage_env == 'db':
    class Review(BaseModel, Base):
        """ Review classto store review information """
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
else:
    class Review(BaseModel):
        place_id = ""
        user_id = ""
        text = ""
