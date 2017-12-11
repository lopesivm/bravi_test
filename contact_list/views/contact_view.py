from flask_restful import Resource, reqparse
from flask.globals import request

from contact_list.controllers import contact_controller

class ContactNoIdView(Resource):
    def post(self):
        try:
            input_json = request.get_json()
            person_id = input_json['person_id']
            contact_value = input_json['contact_value']
            contact_type = input_json['contact_type']
        except:
            return {'error': 'Invalid json input'}, 400
        try:
            contact = contact_controller.add_contact(person_id, contact_value, contact_type)
        except contact_controller.ConContactException as e:
            return {'error': e.message}, 502
        return contact

    def get(self):
        return contact_controller.get_contact()

class ContactIdView(Resource):
    def get(self, contact_id):
        try:
            contact = contact_controller.get_contact(contact_id=contact_id)
        except contact_controller.ContactException as e:
            return {'error': e.message}, 502
        return contact

    def put(self, contact_id):
        try:
            input_json = request.get_json()
            contact_value = input_json['contact_value'] if 'contact_value' in input_json else None
            contact_type = input_json['contact_type'] if 'contact_type' in input_json else None
        except:
            return {'error': 'Invalid json input'}, 400
        try:
            contact = contact_controller.update_contact(contact_id=contact_id,
                                                        contact_value=contact_value,
                                                        contact_type=contact_type)
        except contact_controller.ContactException as e:
            return {'error': e.message}, 502
        return contact

    def delete(self, contact_id):
        try:
            contact = contact_controller.delete_contact(id=contact_id)
        except contact_controller.ContactException as e:
            return {'error': e.message}, 502
        return contact

class ContactSearchView(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('person_id', type=int)
        parser.add_argument('person_name', type=str)
        parser.add_argument('contact_type', type=str)
        args = parser.parse_args()
        person_id = args['person_id'] if 'person_id' in args else None
        person_name = args['person_name'] if 'person_name' in args else None
        contact_type = args['contact_type'] if 'contact_type' in args else None
        try:
            contacts = contact_controller.get_person(person_id=person_id,
                                                     person_name=person_name,
                                                     contact_type=contact_type)
        except contact_controller.ContactException as e:
            return {'error': e.message}, 502
        return contacts