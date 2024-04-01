# Donation Inventory Management REST API

This is a RESTful API built with Python and FastAPI for managing the donation inventory of a local shelter. The API provides endpoints for registering donations, recording distributions, and generating reports.

## Setup

The project is set up as a dev [container](https://code.visualstudio.com/docs/devcontainers/containers). 
Easiest is to run it as such in Visual Studio code. 

Alternatively, install the requirements from the `requirements.txt` file.

```bash
pip3 install -r requirements.txt
```

## Running the API

Run the API server:

```bash
uvicorn main:app --reload
```

The API will be accessible at `http://localhost:8000`.

## API Documentation

You can access the interactive API documentation powered by Swagger UI at `http://localhost:8000/docs` or ReDoc at `http://localhost:8000/redoc`.

## Running Tests

You can run the tests from the terminal:

```
pytest
```

Or you can run the test from Visual Studio Code by clicking the Erlenmeyer lab flask in the toolbar on the left. 

## Bootstrap the data

There is a file `bootstrap_data.sh` that populates some data by running a few curl scripts. 
It might be helpful to then interface with the Swagger UI. 
Run this from the terminal:

```bash
bash bootstrap_data.sh
```


## API Endpoints

### Donors

#### Register a new donor.

```
POST /donor
```

cURL Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "city": "New York"}' http://localhost:8000/donors
```

#### Get donors.

```
GET /donors
```

cURL Example:

```bash
curl -X GET -H "Content-Type: application/json"  http://localhost:8000/donors
```

### Donations

#### Register a new donation.

```
POST /donation
```

cURL Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"donor_id": 1, "donation_type": 3, "quantity": 50.0, "date": "2023-04-01"}' http://localhost:8000/donations
```

#### Get donations.

```
GET /donations
```

cURL Example:

```bash
curl -X GET -H "Content-Type: application/json"  http://localhost:8000/donations
```

### Distribution

#### Record a distribution of donations.

```
POST /distributions
```

**cURL Example:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"donation_id": 1, "quantity": 25.0, "date": "2023-04-02"}' http://localhost:8000/distributions
```

### Get Inventory Report

Get a report of the current donation inventory, grouped by donation type.

```
GET /reports/inventory
```

**cURL Example:**

```bash
curl http://localhost:8000/reports/inventory
```

### Get List of Donors

Get a list of all donors who have made donations.

```
GET /donors
```

**cURL Example:**

```bash
curl http://localhost:8000/donors
```

### Get Donor Report by ID

Get a detailed report for a specific donor, including the total donation amount and a breakdown of individual donations.

```
POST /reports/donors/{donor_id}
```

**cURL Example:**

```bash
curl -X POST http://localhost:8000/reports/donors/1
```

