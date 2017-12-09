from flask import Flask
from flask_restful import Api

from contact_list.views import PersonNoIdView, PersonIdView, PersonSearchView, ContactNoIdView, ContactSearchView, \
    ContactIdView
from contact_list.models import init_engine

app = Flask(__name__)
api = Api(app)

api.add_resource(PersonNoIdView, '/contact_list/person')
api.add_resource(PersonSearchView, '/contact_list/people/search')
api.add_resource(PersonIdView, '/contact_list/person/<person_id>')
api.add_resource(ContactNoIdView, '/contact_list/contact')
api.add_resource(ContactSearchView, '/contact_list/contact/search')
api.add_resource(ContactIdView, '/contact_list/contact/<contact_id>')
init_engine('sqlite:////tmp/contact_list.db')

if __name__ == '__main__':
    app.run(port=5000)