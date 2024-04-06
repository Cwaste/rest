from pydantic import BaseModel

class student_in(BaseModel):
    firstName: str
    middleName: str
    lastName: str
    careerID: int
    controlNumber: str