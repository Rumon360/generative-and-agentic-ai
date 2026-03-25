from pydantic import BaseModel, ConfigDict, Field
from typing import List
from datetime import datetime


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

    # The datetime when the user was created
    created_at: datetime

    # Nested object: each user has one address
    # Pydantic will automatically convert a dictionary into an Address instance
    address: Address

    # List of tags associated with the user
    # default_factory ensures each User instance gets its own list
    tags: List[str] = Field(default_factory=list)

    # ---------------------------
    # Model Configuration
    # ---------------------------
    model_config = ConfigDict(
        # Custom JSON encoder
        # This controls how certain data types are serialized into JSON
        json_encoders={
            # Whenever a datetime is serialized to JSON, use this format
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S")
        }
    )


user_address = Address(street="123", city="Dhaka", zip_code="123")


user = User(
    id=1,
    name="Rumon",
    email="rumon@test.com",
    created_at=datetime(2026, 3, 26, 14, 30),  # creation datetime
    address=user_address,
    is_active=False,
    tags=["premium", "subscriber"],
)

# ---------------------------
# Convert User model to Python dictionary
# ---------------------------
# model_dump() returns a standard Python dict
# Nested models are automatically converted to dicts
python_dict = user.model_dump()


# ---------------------------
# Print human-readable User object
# ---------------------------
print(user)
print("=" * 30)

# Print dictionary representation of the model
# Notice 'created_at' is still a datetime object here
print(python_dict)
print("=" * 30)


# ---------------------------
# Convert User model to JSON string
# ---------------------------
# model_dump_json() returns a JSON string
# Custom JSON encoders (ConfigDict) are applied here
json_str = user.model_dump_json()

# Print JSON output
# 'created_at' is formatted as "dd-mm-yyyy HH:MM:SS"
print(json_str)
