import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import json
import main
from models import *

class TestDonorAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_post_donor(self):
        setup_data()
        donor_data = {
            "first_name": "Joe",
            "last_name": "Bob",
            "city": "Seattle"
        }
        response = self.client.post('/donors', data=json.dumps(donor_data))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data['first_name'], 'Joe')
        self.assertEqual(response_data['last_name'], 'Bob')
        self.assertEqual(response_data['city'], 'Seattle')

    def test_get_donors(self):
        setup_data()
        response = self.client.get("/donors")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(main.donors))
        for i, donor in enumerate(response.json()):
            self.assertEqual(donor["first_name"], main.donors[i].first_name)
            self.assertEqual(donor["last_name"], main.donors[i].last_name)
            self.assertEqual(donor["city"], main.donors[i].city)

    def test_post_donations(self):
        setup_data()
        donation_data = {
            "donor_id": 1,
            "donation_type": 1,
            "quantity": 12,
            "date": "2023-04-01"
        }
        response = self.client.post('/donations', data=json.dumps(donation_data))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data['donor_id'], 1)
        self.assertEqual(response_data['donation_type'], 1)
        self.assertEqual(response_data['quantity'], 12)
        self.assertEqual(response_data['date'], "2023-04-01")

    def test_post_distribution(self):
        setup_data()
        distribution_data = {
            "donation_id": 0,
            "quantity": 1,
            "date": "2023-04-01"
        }
        response = self.client.post('/distributions', data=json.dumps(distribution_data))
        self.assertEqual(response.status_code, 200)

        # try to distribute from the same donation again, but now it should fail 
        response = self.client.post('/distributions', data=json.dumps(distribution_data))
        self.assertEqual(response.status_code, 404)

    def test_reports_inventory(self):
        setup_data()
        response = self.client.get("/reports/inventory")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data[0]['type'], 'DonationType.Money')
        self.assertEqual(len(response_data[0]['donations']), 2)
        self.assertEqual(response_data[1]['type'], 'DonationType.Clothes')
        self.assertEqual(len(response_data[1]['donations']), 1)

    def test_reports_donors(self):
        setup_data()
        response = self.client.get("/reports/donors/1")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data[0]['type'], 'DonationType.Food')
        self.assertEqual(response_data[0]['total'], 12.23)
        self.assertEqual(response_data[1]['type'], 'DonationType.Money')
        self.assertEqual(response_data[1]['total'], 123.2)

def setup_data():
    main.donors = [
        Donor(id=0, first_name="John", last_name="Doe", city="New Jersey"),
        Donor(id=1, first_name="Joe", last_name="Roe", city="New York"),
        Donor(id=2, first_name="Jim", last_name="Boe", city="Seattle")
    ]
    main.donations = [
        Donation(id=0, donor_id=0, donation_type=1, quantity=1.2, date="2023-04-02"),
        Donation(id=1, donor_id=0, donation_type=2, quantity=12.2, date="2023-04-02"),
        Donation(id=2, donor_id=1, donation_type=3, quantity=12.23, date="2023-04-02"),
        Donation(id=3, donor_id=1, donation_type=1, quantity=123.2, date="2023-04-02")
    ]
    main.distributions = [
        Distribution(id=0, donation_id=0, quantity=.2, date="2023-04-02"),
    ]

if __name__ == '__main__':
    unittest.main()
