from pydantic import BaseModel
from typing import List, Dict, Optional


# ---------------------------------------------
# Define a Cart model to represent a shopping cart
# ---------------------------------------------
class Cart(BaseModel):
    user_id: int  # Must be an integer
    items: List[str]  # List of item names (strings)
    quantities: Dict[str, int]  # Dictionary mapping item name → quantity
    # Example: {"Laptop": 1, "Mouse": 2}


# ---------------------------------------------
# Define a BlogPost model
# ---------------------------------------------
class BlogPost(BaseModel):
    title: str  # Blog title (string)
    content: str  # Blog content (string)
    image_url: Optional[str] = None  # Optional field, defaults to None
    # If you don’t provide an image URL, Pydantic automatically sets it to None


# ---------------------------------------------
# Sample cart data (could come from JSON, API, etc.)
# ---------------------------------------------
cart_data = {
    "user_id": 123,
    "items": ["Laptop", "Mouse", "Keyboard"],  # List of items
    "quantities": {
        "Laptop": 1,
        "Mouse": 2,
        "Keyboard": 3,
    },  # Dict mapping items to quantity
}

# Create a Cart instance using unpacking (**cart_data)
# Pydantic automatically validates:
# - user_id is int
# - items is List[str]
# - quantities is Dict[str, int]
cart = Cart(**cart_data)

# Printing cart gives a clean, readable representation
print(cart)
# Output:
# user_id=123 items=['Laptop', 'Mouse', 'Keyboard'] quantities={'Laptop': 1, 'Mouse': 2, 'Keyboard': 3}
