from fastapi import FastAPI
from fastapi.testclient import TestClient
import json
import main
from models import *

def test_post_donor():
    client = TestClient(main.app)
    donor_data = {
            "first_name": "Joe",
            "last_name": "Bob",
            "city": "Seattle"
    }
    
    response = client.post('/donors', data=json.dumps(donor_data))
    assert response.status_code, 200
    response_data = json.loads(response.text)
    assert response_data['first_name'], 'Joe'
    assert response_data['last_name'], 'Bob'
    assert response_data['city'], 'Seattle'

def test_get_donors():
    client = TestClient(main.app)
    main.donors = [
        Donor(id=1, first_name="John", last_name="Doe", city="New York"),
        Donor(id=2, first_name="Jane", last_name="Smith", city="Los Angeles"),
        Donor(id=3, first_name="Bob", last_name="Johnson", city="Chicago"),
    ]
    response = client.get("/donors")
    assert response.status_code, 200
    assert len(response.json()), len(main.donors)
    for i, donor in enumerate(response.json()):
        assert donor["id"], main.donors[i].id
        assert donor["first_name"], main.donors[i].first_name
        assert donor["last_name"], main.donors[i].last_name
        assert donor["city"], main.donors[i].city


def test_post_donations():
    client = TestClient(main.app)
    main.donors = [
        Donor(id=1, first_name="John", last_name="Doe", city="New York")]

    donation_data = {
        "donor_id": 1,
        "donation_type": 1,
        "quantity": 12,
        "date": "2023-04-01"
    }

    response = client.post('/donations', data=json.dumps(donation_data))
    assert response.status_code, 200
    response_data = json.loads(response.text)
    assert response_data['donor_id'], 0
    assert response_data['donation_type'], 1
    assert response_data['quantity'], 12
    assert response_data['date'], 13-3-2023


def test_reports_inventory():
    client = TestClient(main.app)
    main.donors = [
        Donor(id=1, first_name="John", last_name="Doe", city="New York")]

    donation_data = {
        "donor_id": 1,
        "donation_type": 1,
        "quantity": 12.1,
        "date": "2023-04-01"
    }

    client.post('/donations', data=json.dumps(donation_data))
    client.post('/donations', data=json.dumps(donation_data))

    donation_data = {
        "donor_id": 1,
        "donation_type": 2,
        "quantity": 12.2,
        "date": "2023-04-02"
    }

    client.post('/donations', data=json.dumps(donation_data))

    response = client.get("/reports/inventory")

    assert response.status_code, 200
    response_data = json.loads(response.text)
    assert response_data[0]['type'], 'DonationType.Money'
    assert response_data[0]['quantity'], 24.2
    assert response_data[1]['type'], 'DonationType.Clothes'
    assert response_data[1]['quantity'], 12.2

def test_reports_donors():
    client = TestClient(main.app)
    main.donors = [
        Donor(id=1, first_name="John", last_name="Doe", city="New York")]

    donation_data = {
        "donor_id": 1,
        "donation_type": 1,
        "quantity": 12.1,
        "date": "2023-04-01"
    }

    client.post('/donations', data=json.dumps(donation_data))
    client.post('/donations', data=json.dumps(donation_data))

    donation_data = {
        "donor_id": 1,
        "donation_type": 2,
        "quantity": 12.2,
        "date": "2023-04-02"
    }

    client.post('/donations', data=json.dumps(donation_data))

    response = client.get("/reports/donors/1")

    assert response.status_code, 200
    response_data = json.loads(response.text)
    assert response_data[0]['type'], 'DonationType.Money'
    assert response_data[0]['total'], 24.2
    assert response_data[1]['type'], 'DonationType.Clothes'
    assert response_data[1]['total'], 12.3

if __name__ == '__main__':
    test_post_donor()
    test_get_donors()
    test_post_donations()
    test_reports_inventory()
    test_reports_donors()

    #other tests are mechanical
