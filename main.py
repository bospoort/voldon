from fastapi import FastAPI, HTTPException
from typing import List
from models import Donation, Distribution, Donor

donations = []
distributions = []
donors = []

app = FastAPI()

# Donors
@app.post("/donors", response_model=Donor)
def register_donor(donor: Donor):
    donor.id = len(donors) + 1
    donors.append(donor)
    return donor

@app.get("/donors", response_model=List[Donor])
def get_donors():
    return donors

# Donations
@app.post("/donations", response_model=Donation)
def register_donation(donation: Donation):
    found = any(d.id == donation.donor_id for d in donors)
    if not found:
        raise HTTPException(status_code=404, detail="Donor not found")

    if donation.quantity <= 0: 
        raise HTTPException(status_code=404, detail="Invalid amount. Quantity needs to be more than 0.")

    donation.id = len(donations) + 1
    donations.append(donation)
    return donation

@app.get("/donations", response_model=List[Donation])
def get_donations():
    return donations

# Distributions
@app.post("/distributions", response_model=Distribution)
def record_distribution(distribution: Distribution):
    donation = (d.id == distribution.donation_id for d in donations)
    if donation == None:
        raise HTTPException(status_code=404, detail="Donation not found.")
    
    amount_left = donation.quantity
    for existing_distribution in distributions:
        if existing_distribution.donation_id == distribution.donation_id:
            amount_left -= existing_distribution.quantity
    if amount_left < distribution.quantity: 
        raise HTTPException(status_code=404, detail="Not enough of donation left to distribute.")
    
    if distribution.quantity <= 0: 
        raise HTTPException(status_code=404, detail="Invalid amount. Quantity needs to be more than 0.")
    
    # adjust donation amount
    donation.quantity -= distribution.quantity 
    
    distribution.id = len(distributions) + 1
    distributions.append(distribution)
    return distribution

# Reports
@app.get("/reports/inventory", response_model=List[dict])
def get_inventory_report():
    report = {}
    for donation in donations:
        if str(donation.donation_type) in report:
            report[str(donation.donation_type)] += donation.quantity
        else:
            report[str(donation.donation_type)] = donation.quantity
    for distribution in distributions:
        if distribution.donation_type in report:
            report[distribution.donation_type] -= distribution.quantity
    return [{"type": k, "quantity": v} for k, v in report.items()]


@app.get("/reports/donors/{donor_id}", response_model=List[dict])
def get_donor_report(donor_id):
    report = {}
    for donation in donations:
        if donation.donor_id == int(donor_id):
            if str(donation.donation_type) in report:
                report[str(donation.donation_type)] += donation.quantity
            else:        
                report[str(donation.donation_type)] = donation.quantity
    return [{"type": k, "total": v} for k, v in report.items()]
