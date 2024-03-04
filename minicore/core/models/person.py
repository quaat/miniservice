from pydantic import BaseModel, Field
class Person(BaseModel):
    """
    A model representing a person, including their name, email, and age.
    """

    first_name: str = Field(..., description="The person's first name.")
    last_name: str = Field(..., description="The person's last name.")
    email: str = Field(..., description="The person's email address.")
    age: int = Field(..., description="The person's age.")
