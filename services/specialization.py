from sqlalchemy import text
from sqlalchemy.orm import Session

from hospital_app.schemas.specialization import SpecializationCreate, SpecializationUpdate



class SpeService:
    def __init__(self, db: Session):
        self.db = db
    
    def list_all(self) -> list[dict]:
        rows = self.db.execute(
            text("SELECT id, name, doctor_id FROM specializations")
        ).fetchall()

        return [{"id" : r.id, "name" : r.name, "doctor_id" : r.doctor_id} for r in rows]
    
    def get(self, specialization_id : int) -> dict | None:
        row = self.db.execute(
            text("SELECT id, name, doctor_id FROM speciliazations WHERE id = :id"),
            {"id" : specialization_id},
        ).fetchone()

        if row is None:
            return None
        
        return {"id" : row.id, "name" : row.name, "doctor_id" : row.doctor_id}
    
    def create(self, data: SpecializationCreate) -> dict:
        doctor = self.db.execute(
            text("SELECT id from doctors WHERE id= :id"),
            {"id": data.doctor_id},
        ).fetchone()

        if doctor is None:
            return None
        
        specialization = self.db.execute(
            text("INSERT INTO specializations (name, doctor_id) VALUES (:name. :doctor_id)"),
            {"name": data.name, "doctor_id": data.doctor_id},
        )
        
        self.db.commit()
        return self.get(specialization.lastrowid)