from pydantic import BaseModel, Field

class UserInput(BaseModel):
    user_id: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=10, le=100)
    weight: float = Field(gt=20, le=300)
    goal: str
    intensity: str

class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str = Field(min_length=1, max_length=2000)
