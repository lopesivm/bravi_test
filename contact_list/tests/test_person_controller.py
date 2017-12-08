import pytest

from contact_list.models import *
from contact_list.controllers.person_controller import *
from contact_list.models import Person

@pytest.fixture
def db_session(tmpdir):
    init_engine('sqlite:////{}/test.db'.format(tmpdir))
    return get_session()

@pytest.fixture
def person(db_session):
    person_id = add_person('Greg')
    return db_session.query(Person).get(person_id)

@pytest.fixture
def same_people(db_session):
    result = []
    person_id = add_person('Greg')
    result.append(db_session.query(Person).get(person_id))
    person_id = add_person('Greg')
    result.append(db_session.query(Person).get(person_id))
    return result

def test_add_person_success(db_session):
    test_name = 'Greg'
    added_person = add_person(test_name)
    assert added_person['id']
    assert added_person['name'] == test_name
    db_person = db_session.query(Person).get(added_person['id'])
    assert db_person
    assert db_person.id == added_person['id']
    assert db_person.name == added_person['name']

def test_update_person_success(person, db_session):
    test_name = 'Todd'
    updated_person = update_person(person.id, test_name)
    assert updated_person['id'] == person.id
    assert updated_person['name'] == test_name
    db_person = db_session.query(Person).get(updated_person['id'])
    assert db_person
    assert db_person.id == updated_person['id']
    assert db_person.name == updated_person['name']

def test_update_person_not_found_failure(db_session):
    test_name = 'Todd'
    with pytest.raises(Exception):
        update_person(10, test_name)


def test_get_person_by_id_success(person):
    found_person = get_person(id=person.id)
    assert found_person
    assert found_person['id'] == person.id
    assert found_person['name'] == person.name

def test_get_person_by_id_not_found_failure():
    with pytest.raises(Exception):
        get_person(id=10)

def test_get_person_by_name_success(person):
    found_person = get_person(name=person.name)
    assert found_person
    assert isinstance(found_person, list)
    assert len(found_person) == 1
    assert found_person[0]['id'] == person.id
    assert found_person[0]['name'] == person.name

def test_get_people_by_name_success(same_people):
    found_people = get_person(name=same_people[0].name)
    assert found_people
    assert isinstance(found_people, list)
    assert len(found_people) == 2
    assert found_people[0]['id'] in [same_people[0].id, same_people[1].id]
    assert found_people[1]['id'] in [same_people[0].id, same_people[1].id]
    assert found_people[0]['name'] == same_people[0].name
    assert found_people[1]['name'] == same_people[0].name

def test_get_person_by_name_not_found_success():
    found_person = get_person(name='Joseph')
    assert not found_person
    assert isinstance(found_person, list)
    assert len(found_person) == 0

def test_get_person_no_parameter_failure():
    with pytest.raises(Exception):
        get_person()

def test_get_person_both_parameters_failure():
    with pytest.raises(Exception):
        get_person(id=10, name='Joseph')

def test_delete_person_success(person, db_session):
    deleted_person = delete_person(person.id)
    assert deleted_person
    assert deleted_person['id'] == person.id
    assert deleted_person['name'] == person.name
    with pytest.raises(Exception):
        get_person(id=person.id)
    assert len(get_person(name=person.name)) == 0
    db_person = db_session.query(Person).get(person.id)
    assert db_person
    assert db_person.deleted