from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession() 
