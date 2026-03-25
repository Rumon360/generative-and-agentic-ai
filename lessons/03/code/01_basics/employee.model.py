from typing import Optional
from pydantic import BaseModel, Field, EmailStr


# Employee model with advanced field validation
class Employee(BaseModel):
    id: int  # Simple integer field for employee ID

    # Name field with validation rules
    name: str = Field(
        ...,  # '...' means this field is required (cannot be omitted)
        min_length=3,  # Must be at least 3 characters long
        max_length=50,  # Cannot exceed 50 characters
        description="Employee Name",  # Optional metadata, useful in docs (e.g., FastAPI)
        examples="Rumon",  # Example value for auto-generated docs
    )

    # Department is optional; defaults to "General" if not provided
    department: Optional[str] = "General"

    # Salary field with validation
    # ge = greater than or equal (>= 10000)
    salary: float = Field(..., ge=10000)


# User model with complex validation
class User(BaseModel):
    # EmailStr validates proper email format automatically
    email: EmailStr

    # Phone number with regex pattern validation
    # Matches formats like:
    # +12 123-456-7890 or (123) 456-7890
    phone: str = Field(
        ..., pattern=r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"  # Required
    )

    # Age field must be between 0 and 150
    age: int = Field(..., ge=0, le=150, description="Age in years")

    # Discount field must be between 0% and 100%
    discount: float = Field(..., ge=0, le=100, description="Discount percentage")
