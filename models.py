from datetime import date
from typing import Optional
from enum import Enum

from pydantic import BaseModel

class DonationType(Enum):
    Money = 1
    Clothes = 2
    Food = 3

class Donor(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    city: str

class Donation(BaseModel):
    id: Optional[int] = None
    donor_id: int
    donation_type: DonationType
    quantity: float
    date: date

class Distribution(BaseModel):
    id: Optional[int] = None
    donation_id: int
    quantity: float
    date: date

class DonationStatus(BaseModel):
    donation_id: int
    donor_id: int
    quantity: float
    distributed: float = 0.0
