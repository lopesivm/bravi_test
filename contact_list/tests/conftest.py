import pytest

from contact_list import models
from contact_list.controllers import person_controller

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