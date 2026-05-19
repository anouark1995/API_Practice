"""
Doctor ORM model — a Python class that maps to the `doctors` table.

OOP in practice: each row in the DB becomes an instance of this class.
SQLAlchemy reads the class attributes (Column, relationship) to figure out
what the table looks like and how it connects to other tables.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hospital_app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    practice: Mapped[str] = mapped_column(String, nullable=False)
    

    specialization: Mapped["Specialization"] = relationship(
        "Specialization", back_populates="doctor", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Doctor id={self.id} name={self.name!r}>"