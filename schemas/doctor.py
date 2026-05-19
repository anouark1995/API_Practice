from pydantic import BaseModel, ConfigDict


class DoctorCreate(BaseModel):
    """Shape of the JSON the client sends to create a doctor."""
    name: str
    practice: str


class DoctorUpdate(BaseModel):
    """All fields optional — client can update just what they want."""
    name: str | None = None
    practice: str | None = None


class DoctorOut(BaseModel):
    """Shape of the JSON the API sends back."""
    id: int
    name: str
    practice: str

    # Lets Pydantic read attributes off a SQLAlchemy object directly.
    model_config = ConfigDict(from_attributes=True)