@REM Create 3 donors
curl -X POST -H "Content-Type: application/json" -d "{\"first_name\": \"John\", \"last_name\": \"Doe\", \"city\": \"New York\"}" http://localhost:8000/donors
curl -X POST -H "Content-Type: application/json" -d "{\"first_name\": \"Jane\", \"last_name\": \"Smith\", \"city\": \"Los Angeles\"}" http://localhost:8000/donors
curl -X POST -H "Content-Type: application/json" -d "{\"first_name\": \"Bob\", \"last_name\": \"Johnson\", \"city\": \"Chicago\"}" http://localhost:8000/donors

@REM Up to 3 donations per donor
curl -X POST -H "Content-Type: application/json" -d "{\"donor_id\": 1, \"donation_type\": 1, \"quantity\": 100.0, \"date\": \"2023-04-01\"}" http://localhost:8000/donations
curl -X POST -H "Content-Type: application/json" -d "{\"donor_id\": 1, \"donation_type\": 2, \"quantity\": 20.0, \"date\": \"2023-04-02\"}" http://localhost:8000/donations
curl -X POST -H "Content-Type: application/json" -d "{\"donor_id\": 2, \"donation_type\": 3, \"quantity\": 50.0, \"date\": \"2023-04-03\"}" http://localhost:8000/donations
curl -X POST -H "Content-Type: application/json" -d "{\"donor_id\": 2, \"donation_type\": 1, \"quantity\": 75.0, \"date\": \"2023-04-04\"}" http://localhost:8000/donations
curl -X POST -H "Content-Type: application/json" -d "{\"donor_id\": 3, \"donation_type\": 2, \"quantity\": 30.0, \"date\": \"2023-04-05\"}" http://localhost:8000/donations

@REM 4 distributions
curl -X POST -H "Content-Type: application/json" -d "{\"donation_id\": 1, \"quantity\": 50.0, \"date\": \"2023-04-06\"}" http://localhost:8000/distributions
curl -X POST -H "Content-Type: application/json" -d "{\"donation_id\": 2, \"quantity\": 10.0, \"date\": \"2023-04-07\"}" http://localhost:8000/distributions
curl -X POST -H "Content-Type: application/json" -d "{\"donation_id\": 3, \"quantity\": 25.0, \"date\": \"2023-04-08\"}" http://localhost:8000/distributions
curl -X POST -H "Content-Type: application/json" -d "{\"donation_id\": 4, \"quantity\": 40.0, \"date\": \"2023-04-09\"}" http://localhost:8000/distributions