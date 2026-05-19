from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hospital_app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable= False)
    wing: Mapped[int] = mapped_column(ForeignKey("specializations.id"), nullable=False)
    doctor: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)

    specialization: Mapped["Specialization"] = relationship(
        "Specialization", back_populates="patients")
    
    def __repr__(self) -> str:
        return f"<Patient id={self.id} name={self.name!r}>"