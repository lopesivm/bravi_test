import pytest

from contact_list import models
from contact_list.controllers import person_controller, contact_controller

@pytest.fixture
def init_db(tmpdir):
    engine = models.init_engine('sqlite:////{}/test.db'.format(tmpdir))
    return engine

@pytest.fixture
def person(init_db):
    person = person_controller.add_person('Greg')
    session = models.get_session()
    return session.query(models.Person).get(person['id'])

@pytest.fixture
def same_people(init_db):
    result = []
    person = person_controller.add_person('Greg')
    session = models.get_session()
    result.append(session.query(models.Person).get(person['id']))
    person = person_controller.add_person('Greg')
    result.append(session.query(models.Person).get(person['id']))
    return result

@pytest.fixture
def contact(person):
    contact = contact_controller.add_contact(person.id, 'test@email.com', 'email')
    session = models.get_session()
    return session.query(models.Contact).get(contact['id'])

@pytest.fixture
def person_with_contacts(person):
    contact_controller.add_contact(person.id, 'test@email.com', 'email')
    contact_controller.add_contact(person.id, '5511999888777', 'whatsapp')
    contact_controller.add_contact(person.id, '554133332222', 'phone')
    session = models.get_session()
    return session.query(models.Person).get(person.id)

@pytest.fixture
def crowd():
    p = person_controller.add_person('Greg')
    contact_controller.add_contact(p['id'], 'test@email.com', 'email')
    p = person_controller.add_person('Gregory')
    contact_controller.add_contact(p['id'], 'test@email.com', 'email')
    contact_controller.add_contact(p['id'], '5511999888777', 'whatsapp')
    p = person_controller.add_person('McGregor')
    contact_controller.add_contact(p['id'], 'test@email.com', 'email')
    contact_controller.add_contact(p['id'], '5511999888777', 'whatsapp')
    contact_controller.add_contact(p['id'], '554133332222', 'phone')
    session = models.get_session()
    return session.query(models.Person)
