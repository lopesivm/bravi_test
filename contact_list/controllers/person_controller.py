from contact_list import models
from contact_list.controllers.contact_controller import _serialize_contact

def _serialize_person(person):
    return {'id': person.id,
            'name': person.name,
            'contacts': [_serialize_contact(contact) for contact in person.contacts]}

def add_person(name):
    session = models.get_session()
    person = models.Person(name=name)
    session.add(person)
    session.commit()
    return _serialize_person(person)

def update_person(id, name):
    session = models.get_session()
    person = session.query(models.Person).get(id)
    if not person:
        raise PersonNotFoundException('Invalid ID, person not found')
    person.name = name
    session.commit()
    return _serialize_person(person)

def get_person(name=None, id=None):
    session = models.get_session()
    if name and id:
        raise PersonBadParameterException('Only one parameter must be defined')
    elif id:
        person = session.query(models.Person).get(id)
        if not person:
            raise PersonNotFoundException('Invalid ID, person not found')
        result = _serialize_person(person)
    elif name:
        people = session.query(models.Person).filter(models.Person.name.like('%{}%'.format(name)))
        result = [_serialize_person(person) for person in people]
    else:
        people = session.query(models.Person)
        result = [_serialize_person(person) for person in people]
    return result

def delete_person(id):
    session = models.get_session()
    person = session.query(models.Person).get(id)
    if not person:
        raise PersonNotFoundException('Invalid ID, person not found')
    session.delete(person)
    session.commit()
    return _serialize_person(person)

class PersonException(Exception):
    def __init__(self, message):
        self.message = message

class PersonBadParameterException(PersonException):
    pass

class PersonNotFoundException(PersonException):
    pass