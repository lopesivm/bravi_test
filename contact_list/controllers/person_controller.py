from contact_list.models import get_session, Person

def add_person(name):
    session = get_session()
    person = Person(name=name)
    session.add(person)
    session.commit()
    return {'id': person.id,
            'name': person.name,
            'contacts': person.contacts}

def update_person(id, name):
    pass

def get_person(name=None, id=None):
    pass

def delete_person(id):
    pass