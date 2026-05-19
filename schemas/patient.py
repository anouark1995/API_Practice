from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    name: str
    age: int
    wing: int
    doctor: int


class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    wing: int | None = None
    doctor: int | None = None


class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    wing: int
    doctor: int

    model_config = ConfigDict(from_attributes=True)