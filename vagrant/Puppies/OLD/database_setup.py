### Initialize Configuration###

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

###Class, Tables and Mappers ###

class Shelter (Base):

    __tablename__ = 'shelter'

    name = Column(String(20),nullable = False)
    address = Column(String(200))
    city = Column(String(20))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String(100))
    ids = Column(Integer, primary_key = True)

class Puppy (Base):
    
    __tablename__ = 'puppy'

    name = Column(String(20), primary_key = True, nullable = False)
    dob = Column(Date) 
    gender = Column(String(8))
    weight = Column(Integer)
    shelter_id = Column(Integer, ForeignKey('shelter.ids'))
    shelter = relationship(Shelter)

### Complete Configuration###

engine = create_engine('sqlite:///puppies.db')

Base.metadata.create_all(engine)
