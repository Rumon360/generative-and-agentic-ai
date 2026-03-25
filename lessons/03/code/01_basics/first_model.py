from pydantic import BaseModel

# Pydantic models inherit from BaseModel
# They provide:
# 1. Data validation
# 2. Type enforcement
# 3. Easy conversion to/from dict/json


class User(BaseModel):
    """
    Define the schema for a User.
    Pydantic will automatically:
    - Check types when you create an instance
    - Raise errors if data is invalid
    """

    id: int  # User ID must be an integer
    name: str  # Name must be a string
    is_active: bool  # Must be True/False


# Input data (could come from an API, DB, or JSON)
input_data = {"id": 101, "name": "Rumon", "is_active": True}

# Create a User instance
# **input_data → unpack dict into keyword arguments
user = User(**input_data)

# Print the user object
# Pydantic provides a nice __repr__ automatically
print(user)
