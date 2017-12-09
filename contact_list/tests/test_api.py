import pytest
import json

from contact_list.main import app

@pytest.fixture
def client():
    app.testing = True
    test_client = app.test_client()
    return test_client

def test_add_person_endpoint(client):
    test_name = 'Greg'
    response = client.post('/contact_list/person',
                           data=json.dumps({'name': test_name}),
                           headers={'Content-Type': 'application/json'})
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert response_data['name'] == test_name

def test_get_all_people_endpoint(client, same_people):
    response = client.get('/contact_list/person')
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == 2

def test_search_people_endpoint(client, crowd):
    test_name = 'reg'
    query_param = '?name={}'.format(test_name)
    response = client.get('/contact_list/people/search{}'.format(query_param))
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == 3
    for person in response_data:
        assert 'reg' in person['name']

def test_update_person_endpoint(client, person):
    test_name = 'Todd'
    response = client.put('/contact_list/person/{}'.format(person.id),
                           data=json.dumps({'name': test_name}),
                           headers={'Content-Type': 'application/json'})
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert response_data['name'] == test_name

def test_get_person_endpoint(client, person):
    response = client.get('/contact_list/person/{}'.format(person.id))
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert isinstance(response_data, dict)
    assert response_data['name'] == person.name

def test_delete_person_endpoint(client, person):
    response = client.delete('/contact_list/person/{}'.format(person.id))
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert isinstance(response_data, dict)
    assert response_data['name'] == person.name
    response = client.get('/contact_list/person/{}'.format(person.id))
    assert response.status_code == 404