import pytest

from contact_list import models
from contact_list.controllers import contact_controller

def test_add_single_contact_success(person):
    test_value = 'test@email.com'
    test_type = 'email'
    added_contact = contact_controller.add_contact(person.id, test_value, test_type)
    assert added_contact['id']
    assert added_contact['value'] == test_value
    assert added_contact['type'] == test_type
    session = models.get_session()
    db_contact = session.query(models.Contact).get(added_contact['id'])
    assert db_contact
    assert db_contact.id == added_contact['id']
    assert db_contact.value == added_contact['value']
    assert db_contact.type.type_name == added_contact['type']

def test_add_multiple_contact_success(contact):
    test_value = '5511999888777'
    test_type = 'whatsapp'
    added_contact = contact_controller.add_contact(contact.person.id, test_value, test_type)
    assert added_contact['id']
    assert added_contact['value'] == test_value
    assert added_contact['type'] == test_type
    session = models.get_session()
    db_person = session.query(models.Person).get(contact.person.id)
    assert db_person
    assert db_person.contacts
    assert len(db_person.contacts) == 2
    assert test_type in [c.type.type_name  for c in db_person.contacts]
    assert test_value in [c.value for c in db_person.contacts]

def test_add_contact_invalid_person_failure():
    with pytest.raises(contact_controller.ContactException):
        test_value = '5511999888777'
        test_type = 'whatsapp'
        contact_controller.add_contact(10, test_value, test_type)

def test_add_contact_invalid_contact_type_failure(person):
    with pytest.raises(contact_controller.ContactException):
        test_value = '5511999888777'
        test_type = 'telegram'
        contact_controller.add_contact(person.id, test_value, test_type)

def test_update_contact_both_fields_success(contact):
    test_value = '5511999888777'
    test_type = 'whatsapp'
    updated_contact = contact_controller.update_contact(contact.id, test_value, test_type)
    assert updated_contact['id'] == contact.id
    assert updated_contact['value'] == test_value
    assert updated_contact['type'] == test_type
    session = models.get_session()
    db_contact = session.query(models.Column).get(updated_contact['id'])
    assert db_contact
    assert db_contact.id == updated_contact['id']
    assert db_contact.value == updated_contact['value']
    assert db_contact.type.type_name == updated_contact['type']

def test_update_contact_value_only_success(contact):
    test_value = '5511999888777'
    updated_contact = contact_controller.update_contact(contact.id, test_value)
    assert updated_contact['id'] == contact.id
    assert updated_contact['value'] == test_value
    assert updated_contact['type'] == contact.value
    session = models.get_session()
    db_contact = session.query(models.Column).get(updated_contact['id'])
    assert db_contact
    assert db_contact.id == updated_contact['id']
    assert db_contact.value == updated_contact['value']
    assert db_contact.type.type_name == updated_contact['type']

def test_update_contact_type_only_success(contact):
    test_type = 'whatsapp'
    updated_contact = contact_controller.update_contact(contact.id, contact_type=test_type)
    assert updated_contact['id'] == contact.id
    assert updated_contact['value'] == contact.value
    assert updated_contact['type'] == test_type
    session = models.get_session()
    db_contact = session.query(models.Column).get(updated_contact['id'])
    assert db_contact
    assert db_contact.id == updated_contact['id']
    assert db_contact.value == updated_contact['value']
    assert db_contact.type.type_name == updated_contact['type']

def test_update_contact_invalid_contact_id_failure():
    with pytest.raises(contact_controller.ContactException):
        test_value = '5511999888777'
        contact_controller.update_contact(10, test_value)

def test_update_contact_no_updatable_parameters_failure(contact):
    with pytest.raises(contact_controller.ContactException):
        contact_controller.update_contact(contact.id)

def test_update_contact_invalid_contact_type_failure(contact):
    with pytest.raises(contact_controller.ContactException):
        test_type = 'telegram'
        contact_controller.update_contact(contact.id, contact_type=test_type)

def test_get_contact_by_id_success(contact):
    found_contact = contact_controller.get_contact(contact_id=contact.id)
    assert found_contact['id']
    assert found_contact['value'] == contact.value
    assert found_contact['type'] == contact.type.type_name
    assert found_contact['person_name'] == contact.person.name

def test_get_contacts_by_name_single_person_success(person_with_contacts):
    found_contact = contact_controller.get_contact(person_name=person_with_contacts.name)
    assert found_contact
    assert isinstance(found_contact, list)
    assert len(found_contact) == 3
    assert found_contact[0]['name'] == person_with_contacts.name

def test_get_contacts_by_partial_name_multiple_people_success(crowd):
    found_contacts = contact_controller.get_contact(person_name='reg')
    assert found_contacts
    assert isinstance(found_contacts, list)
    assert len(found_contacts) == 6
    assert len([contact for contact in found_contacts if contact['name'] == 'Greg']) == 1
    assert len([contact for contact in found_contacts if contact['name'] == 'Gregory']) == 2
    assert len([contact for contact in found_contacts if contact['name'] == 'McGregor']) == 3

def test_get_contacts_by_person_id_success(person_with_contacts):
    found_contact = contact_controller.get_contact(person_id=person_with_contacts.id)
    assert found_contact
    assert isinstance(found_contact, list)
    assert len(found_contact) == 3
    assert found_contact[0]['name'] == person_with_contacts.name

def test_get_contacts_by_person_name_and_type(person_with_contacts):
    test_type = 'whatsapp'
    found_contact = contact_controller.get_contact(person_name=person_with_contacts.name, contact_type=test_type)
    assert found_contact
    assert isinstance(found_contact, list)
    assert len(found_contact) == 1
    assert found_contact[0]['name'] == person_with_contacts.name

def test_get_contacts_by_person_id_and_type(person_with_contacts):
    test_type = 'whatsapp'
    found_contact = contact_controller.get_contact(person_id=person_with_contacts.id, contact_type=test_type)
    assert found_contact
    assert isinstance(found_contact, list)
    assert len(found_contact) == 1
    assert found_contact[0]['name'] == person_with_contacts.name

def test_get_contacts_contact_type_no_person_identifier_failure(contact):
    with pytest.raises(contact_controller.ContactException):
        contact_controller.get_contact()

def test_get_contact_multiple_identifiers_failure(contact):
    with pytest.raises(contact_controller.ContactException):
        contact_controller.get_contact(contact.id, contact.person.id)

def test_delete_contact_success(contact):
    deleted_contact = contact_controller.delete_contact(contact.id)
    assert deleted_contact
    assert deleted_contact['id'] == contact.id
    assert deleted_contact['value'] == contact.value
    assert deleted_contact['name'] == contact.person.name
    assert deleted_contact['type'] == contact.type.type_name
    with pytest.raises(contact_controller.ContactException):
        contact_controller.get_contact(contact.id)
    assert len(contact_controller.get_contact(person_id=contact.person.id)) == 0
    session = models.get_session()
    assert not session.query(models.Contact).get(contact.id)

def test_delete_contact_invalid_id_failure():
    with pytest.raises(contact_controller.ContactException):
        contact_controller.delete_contact(10)