from pydantic import BaseModel


# Define a Product model using Pydantic
# This automatically enforces types and provides validation
class Product(BaseModel):
    id: int  # Must be an integer
    name: str  # Must be a string
    price: float  # Must be a float
    in_stock: bool = True  # Optional, defaults to True if not provided


# Creating an instance with all fields specified
product_one = Product(id=1, name="Laptop", price=99.99, in_stock=True)
# Product(id=1, name='Laptop', price=99.99, in_stock=True)

# Creating an instance without specifying 'in_stock'
# Pydantic automatically uses the default value True
product_two = Product(id=2, name="Mouse", price=23.33)
# Product(id=2, name='Mouse', price=23.33, in_stock=True)
