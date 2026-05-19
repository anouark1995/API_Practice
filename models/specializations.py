from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hospital_app.database import Base


class Specialization(Base):
    __tablename__ = "specializations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="specialization")
    patients: Mapped[list["Patient"]] = relationship(
        "Patient", back_populates="specialization", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Specialization id={self.id} name={self.name!r}>"