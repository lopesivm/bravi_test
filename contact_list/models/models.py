from datetime import datetime
import inspect
import re

from sqlalchemy import create_engine, Sequence, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, exc, event, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import Pool
from sqlalchemy.types import Text, Boolean, Integer, String
from sqlalchemy.dialects.oracle import DATE

engine = None
db_session = None
Base = declarative_base()

def init_engine(uri, **kwargs):
    global engine
    global db_session
    engine = create_engine(uri, **kwargs)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine, autocommit=False)
    return engine

def get_session():
    return db_session()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    contacts = relationship('Contact', backref='person')

class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    value = Column(String(255), nullable=False)
    type = relationship('ContactType')

class ContactType(Base):
    __tablename__ = 'contact_type'
    id = Column(Integer, primary_key=True)
    type_name = Column(String(25))