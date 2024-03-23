#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
# import json
import os
from sqlalchemy import (create_engine)


class DBStorage:
    """This class manages db storage of hbnb models"""
    __engine = None
    __session = None
    #    __objects = {}

    def __init__(self):
        """ Initialize method for dbStorage"""
        # retrieve environment variables
        storage_env = os.environ.get('HBNB_TYPE_STORAGE')
        db_name = os.environ.get('HBNB_MYSQL_DB')
        host = os.environ.get('HBNB_MYSQL_HOST')
        password = os.environ.get('HBNB_MYSQL_PWD')
        user = os.environ.get('HBNB_MYSQL_USER')
        running_env = os.environ.get('HBNB_ENV')

        # create engine

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                        user,
                        password,
                        host,
                        db_name), pool_pre_ping=True)

        # for HBNB_ENV == test, drop all tables
        if running_env == 'test':
            # Reflect existing tables from the database
            metadata = MetaData(bind=self.__engine)
            metadata.reflect()
            # Drop all tables
            metadata.drop_all()

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage

            Args:
                cls: class whose objects' should be returned
        """
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {
                    'User': User, 'Place': Place, 'State': State,
                    'City': City, 'Amenity': Amenity, 'Review': Review
                  }
        classes_names = {
                    User: 'User', Place: 'Place', State: 'State',
                    City: 'City', Amenity: 'Amenity', Review: 'Review'
                  }

        if cls:
            objs_list = self.__session.query(cls).all()
            new_dictionary = {"{}.{}".format(
                        classes_names[cls], obj.id): obj for obj in objs_list}
            return new_dictionary
        else:
            # loop through all classes and retrieve objects
            objs_dict = {}
            for class_type in classes.values():
                objs_list = self.__session.query(class_type).all()
                # traverse thru list and add to objs_dict
                for obj in objs_list:
                    objs_dict.update({"{}.{}".format(
                        classes_names[class_type], obj.id): obj})
            return objs_dict

    def new(self, obj):
        """Adds new object to database"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to database"""
        self.__session.commit()

    def reload(self):
        """create all tables in database and assign a session"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        # create session
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.orm import scoped_session
        session_factory = sessionmaker(
                        bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def delete(self, obj=None):
        """ delete obj from __objects

            Args:
                obj: object to be deleted
        """
        if obj:
            self.__session.delete(obj)
            self.save()
