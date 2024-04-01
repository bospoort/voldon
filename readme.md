

## Interaction

Register a donor:

``
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "city": "Tacoma"}' http://localhost:8000/donors
``

Retrieve a list of donors:

``
curl http://localhost:8000/donors
``