#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
# from models.place import Place
# from models.review import Review
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import os
storage_env = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if storage_env == 'db':    
        __tablename__ = 'users'
        first_name = Column(String(128))
        last_name = Column(String(128))
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        places = relationship("Place", cascade="all, delete", backref="user")
        reviews = relationship("Review", cascade="all, delete", backref="user")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
