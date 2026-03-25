from pydantic import BaseModel, computed_field, Field


# Product model to represent an item with price and quantity
class Product(BaseModel):
    price: float  # price of a single item
    quantity: int  # number of items

    # computed_field makes this value part of the model output (like model_dump)
    # @property allows accessing it like an attribute (product.total_price)
    @computed_field
    @property
    def total_price(self) -> float:
        # This value is dynamically calculated, not stored
        return self.price * self.quantity


# Booking model to represent a hotel/room booking
class Booking(BaseModel):
    user_id: int
    room_id: int

    # Field(..., ge=1) means:
    # ...  -> this field is required
    # ge=1 -> value must be >= 1 (greater than or equal to 1)
    nights: int = Field(..., ge=1)

    rate_per_night: float

    # computed_field will include this in serialized output
    @computed_field
    @property
    def total_amount(self) -> float:
        # total cost = number of nights × price per night
        return self.nights * self.rate_per_night


# Create an instance of Booking
booking = Booking(user_id=123, room_id=234, nights=3, rate_per_night=100)

# Access computed property like a normal attribute
print(booking.total_amount)  # Output: 300

# model_dump() converts the model into a dictionary
# computed fields are INCLUDED by default
print(booking.model_dump())
