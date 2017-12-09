from flask_restful import Resource
from flask.globals import request
from flask_restful import reqparse

from contact_list.controllers import person_controller

class PersonNoIdView(Resource):
    def post(self):
        try:
            input_json = request.get_json()
            name = input_json['name']
        except:
            return {'error': 'Invalid json input'}, 400
        try:
            person = person_controller.add_person(name)
        except person_controller.PersonException as e:
            return {'error': e.message}, 502
        return person

    def get(self):
        return person_controller.get_person()

class PersonSearchView(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        name = args['name'] if 'name' in args else None
        try:
            people = person_controller.get_person(name=name)
        except person_controller.PersonBadParameterException as e:
            return {'error': e.message}, 400
        except person_controller.PersonException as e:
            return {'error': e.message}, 502
        return people


class PersonIdView(Resource):
    def get(self, person_id):
        try:
            person = person_controller.get_person(id=person_id)
        except person_controller.PersonNotFoundException as e:
            return {'error': e.message}, 404
        except person_controller.PersonException as e:
            return {'error': e.message}, 502
        return person

    def put(self, person_id):
        try:
            input_json = request.get_json()
            name = input_json['name']
        except:
            return {'error': 'Invalid json input'}, 400
        try:
            person = person_controller.update_person(person_id, name)
        except person_controller.PersonNotFoundException as e:
            return {'error': e.message}, 404
        except person_controller.PersonException as e:
            return {'error': e.message}, 502
        return person

    def delete(self, person_id):
        try:
            person = person_controller.delete_person(id=person_id)
        except person_controller.PersonNotFoundException as e:
            return {'error': e.message}, 404
        except person_controller.PersonException as e:
            return {'error': e.message}, 502
        return person