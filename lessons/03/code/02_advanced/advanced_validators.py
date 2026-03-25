from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime


# Model representing a person with first and last name
class Person(BaseModel):
    first_name: str
    last_name: str

    # Validate multiple fields at once
    @field_validator("first_name", "last_name")
    def names_must_be_capitalize(cls, v):
        # istitle() checks if the string is capitalized properly (e.g., "John")
        if not v.istitle():
            raise ValueError("Names must be capitalized")
        return v


# Model representing a user with email
class User(BaseModel):
    email: str  # ⚠️ FIX: field name must match validator

    # This validator runs for the "email" field
    @field_validator("email")
    def normalize_email(cls, v):
        # Normalize email: remove spaces and convert to lowercase
        return v.lower().strip()


# Model representing a product with price
class Product(BaseModel):
    price: float  # ⚠️ Better to store as float after parsing

    # mode="before" means this runs BEFORE type validation
    @field_validator("price", mode="before")
    def parse_price(cls, v):
        # If input is a string like "$10", convert it to float
        if isinstance(v, str):
            return float(v.replace("$", ""))
        return v


# Model representing a date range
class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    # model-level validation (checks multiple fields together)
    @model_validator(mode="after")
    def validate_date_range(cls, values):
        # Ensure start_date is before end_date
        if values.start_date >= values.end_date:
            raise ValueError("end_date must after start_date")
        return values
