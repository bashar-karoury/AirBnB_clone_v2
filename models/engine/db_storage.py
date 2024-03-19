#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
# import json
import os

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
        
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}}:3306/{}'.format(
                        user,
                        password,
                        host,
                        db_name), pool_pre_ping=True)
        
        # create session
        from sqlalchemy.orm import sessionmaker
        self.__session = sessionmaker(bind=self.__engine)
    
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
        session = self.__session()
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {
                    'User': User, 'Place': Place, 'State': State,
                    'City': City, 'Amenity': Amenity,'Review': Review
                  }
        classes_names = {
                    User: 'User', Place: 'Place', State: 'State',
                    City: 'City', Amenity: 'Amenity',Review: 'Review'
                  }    

        
        san_fran = session.query(cls).all()
        if cls:
            objs_list = session.query(cls).all()
            return {"{}.{}".format(classes_names[cls], obj.id): obj for obj in objs_list}
        else:
            # loop through all classes and retrieve objects
            objs_dict = {}
            for class_type in classes.values():
                objs_list = session.query(class_type).all()
                # traverse thru list and add to objs_dict
                for obj in objs_list: 
                    objs_dict.update("{}.{}".format(classes_names[class_type], obj.id) = obj)
            return objs_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete obj from __objects

            Args:
                obj: object to be deleted
        """
        if obj:
            for key, o in FileStorage.__objects.items():
                if o == obj:
                    del (FileStorage.__objects)[key]
                    break
            del obj
            self.save()
