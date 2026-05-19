from pydantic import BaseModel, ConfigDict


class SpecializationCreate(BaseModel):
    name: str
    doctor_id: int


class SpecializationUpdate(BaseModel):
    name: str | None = None
    doctor_id: int | None = None


class SpecializationOut(BaseModel):
    id: int
    name: str
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)