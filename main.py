from fastapi import FastAPI, HTTPException
from typing import List
from models import *

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

    matches = [d for d in donations if d.id == distribution.donation_id]
    if matches == False:
        raise HTTPException(status_code=404, detail="Donation not found.")
    
    amount_left = matches[0].quantity
    for existing_distribution in distributions:
        if existing_distribution.donation_id == distribution.donation_id:
            amount_left -= existing_distribution.quantity
    if amount_left < distribution.quantity: 
        raise HTTPException(status_code=404, detail="Not enough of donation left to distribute.")
    
    if distribution.quantity <= 0: 
        raise HTTPException(status_code=404, detail="Invalid amount. Quantity needs to be more than 0.")
    
    distribution.id = len(distributions) + 1
    distributions.append(distribution)
    return distribution

def get_donation_status(donation):
    matches = [dist for dist in distributions if dist.donation_id == donation.id]
    total_distributed = sum(dist.quantity for dist in matches)
    return DonationStatus(
        donation_id=donation.id, 
        donor_id=donation.donor_id,
        quantity=donation.quantity,
        distributed=donation.quantity-total_distributed
    )

# Reports
@app.get("/reports/inventory", response_model=List[dict])
def get_inventory_report():
    report = {}
    for donation in donations:
        status = get_donation_status(donation)
        if str(donation.donation_type) in report:
            report[str(donation.donation_type)].append(status)
        else:
            report[str(donation.donation_type)] = [status]

    result = []
    for donation_type, donations_list in report.items():
        donation_type_dict = {
            "type": donation_type,
            "donations": donations_list
        }
        result.append(donation_type_dict)

    return result

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
