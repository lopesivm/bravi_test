# Bravi Test for Ivan Lopes

## Requirements
* Python 3, with it's binary on system's path
* Linux environment

## Setup
While on the root of the test directory execute the setup script. 
This will:
* run Python's virtualenv binary, creating a new virtual environment on venv folder
* install the test's Python dependencies listed on requirements.txt
* run all available tests for the projects

## Testing
All available tests for the projects can be run by executing the scrit ```./run_tests```
Due to time constraints, the project Weather in my city has no tests, being the only project not following TDD.

## Running the projects
All projects have a script named ```exec_<project_name>```, that will use the correct python binary from the venv folder, and run the project. Below are the details per project.

### Balanced Brackets
Run the exec_balanced_brackets script, passing strings enclosed in quotes as parameters to be validated by the software.
Examples:
```./exec_balanced_brackets '[{()}]'```
```./exec_balanced_brackets '[({})([])]' '(){}[]' '{()}{)' '()(0){}'```

### Contact List
Run the exec_contact_list script to run the server on [port 5001](http://localhost:5001).
The endpoints and their usage are listed below:
#### Add person
```
[**POST**] /contact_list/person
**Data Params** (JSON) {"name": <person_name>}
**Query Params** None
**Returns** (JSON) {"id": <person_id>, "name": <person_name>, "contacts": [<list_of_contacts>]}
```

#### Get all people
```
[**GET**] /contact_list/person
**Data Params** None
**Query Params** None
**Returns** (JSON) List of people
```

#### People search
```
[**GET**] /contact_list/people/search
**Data Params** None
**Query Params** ?name=<person_name>
**Returns** (JSON) List of people
```

#### Get person by id
```
[**GET**] /contact_list/person/<person_id>
**Data Params** None
**Query Params** None
**Returns** (JSON) {"id": <person_id>, "name": <person_name>, "contacts": [<list_of_contacts>]}
```

#### Update person
```
[**PUT**] /contact_list/person/<person_id>
**Data Params** (JSON) {"name": <person_name>}
**Query Params** None
**Returns** (JSON) {"id": <person_id>, "name": <person_name>, "contacts": [<list_of_contacts>]}
```

#### Delete person
```
[**DELETE**] /contact_list/person/<person_id>
**Data Params** None
**Query Params** None
**Returns** (JSON) {"id": <person_id>, "name": <person_name>, "contacts": [<list_of_contacts>]}
```

#### Add contact
```
[**POST**] /contact_list/contact
**Data Params** (JSON) {"person_id": <person_id>, "contact_value": <contact_value>, "contact_type": <contact_type>} (Available contact types are 'email', 'phone' or 'whatsapp')
**Query Params** None
**Returns** (JSON) {"id": <contact_id>, "value": <contact_value>, "name": <person_name>, "type": <contact_type>}
```

#### Get all contacts
```
[**GET**] /contact_list/contact
**Data Params** None
**Query Params** None
**Returns** (JSON) List of contacts
```

#### Contacts search
```
[**GET**] /contact_list/contact/search
**Data Params** None
**Query Params** ?person_id=<person_id> | ?person_name=<person_name> | ?contact_type=<contact_type> (only person_id OR person_name might be set on a search)
**Returns** (JSON) List of contacts
```

#### Get contact by id
```
[**GET**] /contact_list/contact/<contact_id>
**Data Params** None
**Query Params** None
**Returns** (JSON) {"id": <contact_id>, "value": <contact_value>, "name": <person_name>, "type": <contact_type>}
```

#### Update contact
```
[**PUT**] /contact_list/contact/<contact_id>
**Data Params** (JSON) {"contact_value": <contact_value>, "contact_type": <contact_type>}
**Query Params** None
**Returns** (JSON) {"id": <contact_id>, "value": <contact_value>, "name": <person_name>, "type": <contact_type>}
```

#### Delete contact
```
[**DELETE**] /contact_list/contact/<contact_id>
**Data Params** None
**Query Params** None
**Returns** (JSON) {"id": <contact_id>, "value": <contact_value>, "name": <person_name>, "type": <contact_type>}
```

### Weather in my city
Run the exec_weather_in_my_city script to run the server on [port 5002](http://localhost:5002). All process should be intuitive from the single-page web application.
