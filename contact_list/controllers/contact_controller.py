from contact_list import models

def _serialize_contact(contact):
    return {'id': contact.id,
            'value': contact.value,
            'name': contact.person.name,
            'type': contact.type.type_name}

def add_contact(person_id, contact_value, contact_type):
    session = models.get_session()
    try:
        type = session.query(models.ContactType).filter(models.ContactType.type_name == contact_type).one()
    except:
        raise ContactException('Invalid contact type')
    if not session.query(models.Person).get(person_id):
        raise ContactException('Invalid Person ID, person not found')
    contact = models.Contact(person_id=person_id, type_id=type.id, value=contact_value)
    session.add(contact)
    session.commit()
    return _serialize_contact(contact)

def update_contact(contact_id, contact_value=None, contact_type=None):
    session = models.get_session()
    contact = session.query(models.Contact).get(contact_id)
    if not contact:
        raise ContactException('Invalid ID, contact not found')
    if not contact_type and not contact_value:
        raise ContactException('At least one updatable parameter must be specified')
    if contact_value:
        contact.value = contact_value
    if contact_type:
        try:
            type = session.query(models.ContactType).filter(models.ContactType.type_name == contact_type).one()
        except:
            raise ContactException('Invalid contact type')
        contact.type_id = type.id
    session.commit()
    return _serialize_contact(contact)

def get_contact(contact_id=None, person_id=None, person_name=None, contact_type=None):
    session = models.get_session()
    if (contact_id and (person_id or person_name) or (person_id and person_name)):
        raise ContactException('Too many parameters, specify either contact_id, person_id or person_name')
    if not contact_id and not person_id and not person_name:
        contacts = session.query(models.Contact)
        result = [_serialize_contact(contact) for contact in contacts]
    if contact_id:
        contact = session.query(models.Contact).get(contact_id)
        if not contact:
            raise ContactException('Invalid ID, contact not found')
        result = _serialize_contact(contact)
    elif person_id or person_name:
        contacts = session.query(models.Contact)
        if contact_type:
            contacts = contacts.join(models.ContactType).filter(models.ContactType.type_name==contact_type)
        if person_id:
            contacts = contacts.filter(models.Contact.person_id == person_id)
        elif person_name:
            contacts = contacts.join(models.Person).filter(models.Person.name.like('%{}%'.format(person_name)))
        result = [_serialize_contact(contact) for contact in contacts]
    return result


def delete_contact(id):
    session = models.get_session()
    contact = session.query(models.Contact).get(id)
    if not contact:
        raise ContactException('Invalid ID, contact not found')
    result = _serialize_contact(contact)
    session.delete(contact)
    session.commit()
    return result

class ContactException(Exception):
    pass