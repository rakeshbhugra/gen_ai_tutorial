class User:
    def __init__(self, name: str, age: int, email: str = None):
        self.name = name
        self.age = age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        if age <= 0:
            raise ValueError("Age must be a positive integer")

        self.email = email
        if email and "@" not in email:
            raise ValueError("Invalid email address")

user = User(name="alice", age=30, email="someoneexample.com")
print(user.name, user.age)


sql_query = "SELECT * FROM users WHERE age > 30"
# This SQL query will fail because age is an integer field, there is no validation 


# How we can use pydantic to solve this problem

from pydantic import BaseModel, Field, EmailStr, ValidationError

class UserModel(BaseModel):
    name: str
    age: int = Field(..., gt=0, description="Age must be a positive integer")
    email: EmailStr = None  # Using EmailStr for built-in email validation

try:
    user = UserModel(name="alice", age=-1, email="someone@example.com")
    print(user.name, user.age, user.email)
except ValidationError as e:
    print("Validation error:", e)