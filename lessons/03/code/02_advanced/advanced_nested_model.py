from pydantic import BaseModel
from typing import Optional, Union, List


# ---------------------------
# Basic Nested Models
# ---------------------------


class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class Company(BaseModel):
    name: str

    # Optional means this field can be:
    # - an Address object
    # - or None (default)
    address: Optional[Address] = None


class Employee(BaseModel):
    name: str

    # Company is also optional
    # You can pass a dict or Company instance
    company: Optional[Company] = None


# ---------------------------
# Mixed Data Types (Union)
# ---------------------------


class TextContent(BaseModel):
    text: str
    content: str


class ImageContent(BaseModel):
    image: str
    url: str
    alt_text: str


# This model accepts multiple possible types inside a list
class Article(BaseModel):
    title: str

    # Each item in sections can be:
    # - TextContent OR ImageContent
    sections: List[Union[TextContent, ImageContent]]


# ---------------------------
# Deeply Nested Structure
# ---------------------------


class Country(BaseModel):
    name: str
    code: str


class State(BaseModel):
    name: str

    # Nested inside State
    country: Country


class City(BaseModel):
    name: str

    # Nested inside City
    state: State


# ⚠️ NOTE: This redefines Address (overwrites the earlier one)
# In real projects, use different names to avoid confusion
class Address(BaseModel):
    street: str

    # Now city is not a string, but a full City object
    city: City

    postal_code: str


class Organization(BaseModel):
    name: str

    # A single nested Address
    head_quarter: Address

    # List of nested Address objects
    # ⚠️ Avoid using [] as default (mutable default issue)
    # Better: use Field(default_factory=list)
    branches: List[Address] = []
