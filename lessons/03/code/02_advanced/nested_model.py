from pydantic import BaseModel


# Nested model representing an address
class Address(BaseModel):
    street: str
    city: str
    postal_code: str


# User model that includes another model (Address)
class User(BaseModel):
    id: str  # Pydantic will auto-convert types if possible (e.g., int → str)
    name: str
    address: Address  # Nested model


# Create an Address instance manually
address = Address(street="123", city="Dhaka", postal_code="123")

# Pass the Address object directly into User
user = User(id="1", name="Rumon", address=address)


# Raw input data (like from API or JSON)
user_data = {
    "id": 1,  # int instead of str → Pydantic will convert to "1"
    "name": "Rumon",
    "address": {  # Nested dictionary instead of Address object
        "street": "123",
        "city": "Dhaka",
        "postal_code": "123",
    },
}

# Pydantic automatically:
# - Converts id from int → str
# - Converts address dict → Address object
user2 = User(**user_data)
