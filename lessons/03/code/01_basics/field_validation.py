from pydantic import BaseModel, field_validator, model_validator


# Define a model for a user
class User(BaseModel):
    # This field must be a string
    username: str

    # field_validator is used to validate a single field
    # It runs automatically when a User instance is created
    @field_validator("username")
    def username_length(cls, v):
        # 'v' is the value of the username field

        # Check if username length is less than 4 characters
        if len(v) < 4:
            # Raise an error if validation fails
            raise ValueError("Username must be at least 4 characters")

        # Always return the validated (or modified) value
        return v


# Define another model for signup data
class SignupDate(BaseModel):
    password: str
    confirm_password: str

    # model_validator is used to validate multiple fields together
    # mode="after" means this runs AFTER all fields are validated individually
    @model_validator(mode="after")
    def password_match(cls, values):
        # 'values' is the full model instance (not a dict in Pydantic v2)

        # Check if both password fields match
        if values.password != values.confirm_password:
            # Raise an error if they don't match
            raise ValueError("Passwords do no match")

        # Return the validated model instance
        return values
