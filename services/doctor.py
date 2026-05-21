from sqlalchemy import text
from sqlalchemy.orm import Session

from hospital_app.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[dict]:
        rows = self.db.execute(text("SELECT id, name, practice FROM doctors")).fetchall()
        print(rows)
        return [{"id": r.id, "name": r.name, "practice": r.practice} for r in rows]

    def get(self, doctor_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT id, name, practice FROM doctors WHERE id = :id"),
            {"id": doctor_id},
        ).fetchone()
        if row is None:
            return None
        return {"id": row.id, "name": row.name, "practice": row.practice}

    def create(self, data: DoctorCreate) -> dict:
        print("THE DATA IS", data)
        result = self.db.execute(
            text("INSERT INTO doctors (name, practice) VALUES (:name, :practice)"),
            {"name": data.name, "practice": data.practice},
        )
        self.db.commit()
        new_id = result.lastrowid
        return self.get(new_id)

    def update(self, doctor_id: int, data: DoctorUpdate) -> dict | None:
        if self.get(doctor_id) is None:
            return None
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            return self.get(doctor_id)
        set_clause = ", ".join(f"{col} = :{col}" for col in fields)
        fields["id"] = doctor_id
        self.db.execute(
            text(f"UPDATE doctors SET {set_clause} WHERE id = :id"),
            fields,
        )
        self.db.commit()
        return self.get(doctor_id)

    def delete(self, doctor_id: int) -> bool:
        if self.get(doctor_id) is None:
            return False
        self.db.execute(
            text("DELETE FROM doctors WHERE id = :id"),
            {"id": doctor_id},
        )
        self.db.commit()
        return True
