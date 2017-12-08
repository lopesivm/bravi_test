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

def test_add_person_success(init_db):
    test_name = 'Greg'
    added_person = person_controller.add_person(test_name)
    assert added_person['id']
    assert added_person['name'] == test_name
    session = models.get_session()
    db_person = session.query(models.Person).get(added_person['id'])
    assert db_person
    assert db_person.id == added_person['id']
    assert db_person.name == added_person['name']

def test_update_person_success(person):
    test_name = 'Todd'
    updated_person = person_controller.update_person(person.id, test_name)
    assert updated_person['id'] == person.id
    assert updated_person['name'] == test_name
    session = models.get_session()
    db_person = session.query(models.Person).get(updated_person['id'])
    assert db_person
    assert db_person.id == updated_person['id']
    assert db_person.name == updated_person['name']

def test_update_person_not_found_failure(init_db):
    test_name = 'Todd'
    with pytest.raises(Exception):
        person_controller.update_person(10, test_name)


def test_get_person_by_id_success(person):
    found_person = person_controller.get_person(id=person.id)
    assert found_person
    assert found_person['id'] == person.id
    assert found_person['name'] == person.name

def test_get_person_by_id_not_found_failure(init_db):
    with pytest.raises(Exception):
        person_controller.get_person(id=10)

def test_get_person_by_name_success(person):
    found_person = person_controller.get_person(name=person.name)
    assert found_person
    assert isinstance(found_person, list)
    assert len(found_person) == 1
    assert found_person[0]['id'] == person.id
    assert found_person[0]['name'] == person.name

def test_get_people_by_name_success(same_people):
    found_people = person_controller.get_person(name=same_people[0].name)
    assert found_people
    assert isinstance(found_people, list)
    assert len(found_people) == 2
    assert found_people[0]['id'] in [same_people[0].id, same_people[1].id]
    assert found_people[1]['id'] in [same_people[0].id, same_people[1].id]
    assert found_people[0]['name'] == same_people[0].name
    assert found_people[1]['name'] == same_people[0].name

def test_get_person_by_name_not_found_success(init_db):
    found_person = person_controller.get_person(name='Joseph')
    assert not found_person
    assert isinstance(found_person, list)
    assert len(found_person) == 0

def test_get_person_no_parameter_failure(init_db):
    with pytest.raises(Exception):
        person_controller.get_person()

def test_get_person_both_parameters_failure(init_db):
    with pytest.raises(Exception):
        person_controller.get_person(id=10, name='Joseph')

def test_delete_person_success(person, init_db):
    deleted_person = person_controller.delete_person(person.id)
    assert deleted_person
    assert deleted_person['id'] == person.id
    assert deleted_person['name'] == person.name
    with pytest.raises(Exception):
        person_controller.get_person(id=person.id)
    assert len(person_controller.get_person(name=person.name)) == 0
    session = models.get_session()
    assert not session.query(models.Person).get(person.id)

def test_delete_invalid_id_failure(init_db):
    with pytest.raises(Exception):
        person_controller.delete_person(10)