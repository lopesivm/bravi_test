from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import Integer, String, Boolean

engine = None
db_session = None
Base = declarative_base()

def init_engine(uri, **kwargs):
    global engine
    global db_session
    engine = create_engine(uri, **kwargs)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine, autocommit=False)
    if not db_session().query(ContactType.id).count():
        insert_initial_contact_types()
    return engine

def get_session():
    return db_session()

def insert_initial_contact_types():
    session = db_session()
    for type in ['phone', 'email', 'whatsapp']:
        session.add(ContactType(type_name=type))
    session.commit()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    deleted = Column(Boolean, default=False)
    contacts = relationship('Contact', backref='person')

class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('contact_type.id'), nullable=False)
    value = Column(String(255), nullable=False)
    deleted = Column(Boolean, default=False)
    type = relationship('ContactType')

class ContactType(Base):
    __tablename__ = 'contact_type'
    id = Column(Integer, primary_key=True)
    type_name = Column(String(25), unique=True, nullable=False)