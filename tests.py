from fastapi import FastAPI
from fastapi.testclient import TestClient
import json
import main
from models import *

def test_post_donor():
    setup_data()
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
    setup_data()
    response = client.get("/donors")
    assert response.status_code, 200
    assert len(response.json()), len(main.donors)
    for i, donor in enumerate(response.json()):
        assert donor["first_name"], main.donors[i].first_name
        assert donor["last_name"], main.donors[i].last_name
        assert donor["city"], main.donors[i].city


def test_post_donations():
    setup_data()

    donation_data = {
        "donor_id": 1,
        "donation_type": 1,
        "quantity": 12,
        "date": "2023-04-01"
    }

    response = client.post('/donations', data=json.dumps(donation_data))
    assert response.status_code, 200
    response_data = json.loads(response.text)
    assert response_data['donor_id'], 1
    assert response_data['donation_type'], 1
    assert response_data['quantity'], 12
    assert response_data['date'], 13-3-2023


def test_reports_inventory():
    setup_data()

    response = client.get("/reports/inventory")

    assert response.status_code, 200
    response_data = json.loads(response.text)
    assert response_data[0]['type'], 'DonationType.Money'
    assert response_data[0]['quantity'], 24.2
    assert response_data[1]['type'], 'DonationType.Clothes'
    assert response_data[1]['quantity'], 12.2

def test_reports_donors():
    setup_data()

    response = client.get("/reports/donors/1")

    assert response.status_code, 200
    response_data = json.loads(response.text)
    assert response_data[0]['type'], 'DonationType.Food'
    assert response_data[0]['total'], 12.2
    assert response_data[1]['type'], 'DonationType.Money'
    assert response_data[1]['total'], 123.2

def setup_data():
    main.donors = [
        Donor(id=0, first_name="John", last_name="Doe", city="New Jersey"),
        Donor(id=1, first_name="Joe", last_name="Roe", city="New York"),
        Donor(id=2, first_name="Jim", last_name="Boe", city="Seattle")]

    main.donations = [
        Donation(id=0, donor_id=0, donation_type=1, quantity=1.2, date="2023-04-02"),
        Donation(id=1, donor_id=0, donation_type=2, quantity=12.2, date="2023-04-02"),
        Donation(id=2, donor_id=1, donation_type=3, quantity=12.23, date="2023-04-02"),
        Donation(id=3, donor_id=1, donation_type=1, quantity=123.2, date="2023-04-02")]
    
    main.distributions = []

if __name__ == '__main__':
    client = TestClient(main.app)
    test_post_donor()
    test_get_donors()
    test_post_donations()
    test_reports_inventory()
    test_reports_donors()