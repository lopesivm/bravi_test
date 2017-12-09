def add_contact(person_id, contact_value, contact_type):
    pass

def update_contact(contact_id, contact_value=None, contact_type=None):
    pass

def get_contact(contact_id=None, person_id=None, person_name=None, contact_type=None):
    pass

def delete_contact(id):
    pass

class ContactException(Exception):
    pass