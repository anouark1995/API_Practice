from sqlalchemy import text
from sqlalchemy.orm import Session

from hospital_app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, db: Session):
        self.db = db
    
    def list_all(self) -> list[dict]:
        rows = self.db.execute(
            text("SELECT name, age, wing, doctor FROM patients")
        ).fetchall()

        return [{"name" : r.name, "age" : r.age, "wing" : r.wing, "doctor" : r.doctor} for r in rows]
    
    def get(self, patient_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT name, age, wing, doctor FROM patients WHERE id = :id"),
            {"id" : patient_id},
        ).fetchone()
        if row is None:
            return None
        return {"name" : row.name, "age" : row.age, "wing" : row.wing, "doctor" : row.doctor }
    
    def create(self, data: PatientCreate ) -> dict:
        spe = self.db.execute(
            text("SELECT id from specilaizations WHERE id= :id"),
            {"id": data.wing}
        )
        if spe is None:
            return None
        
        patient = self.db.execute(
            text("INSERT INTO patients (name, age, wing, doctor) VALUES (:name, :age, :wing, :doctor)"),
            {"name" : data.name, "age" : data.age, "wing" : data.wing, "doctor": data.doctor},
        )

        self.db.commit()
        return self.get(patient.lastrowid)
    
    def update(self, patient_id: int, data: PatientUpdate) -> dict | None:
        if self.get(patient_id) is None:
            return None
        
        fields = data.model_dump(exclude_unset=True)

        if not fields:
            return self.get(patient_id)
        
        set_clause = ", ".join(f"{col} = :{col}" for col in fields)
        fields["id"] = patient_id
        self.db.execute(
            text(f"UPDATE patients SET {set_clause} WHERE id= :id"),
            fields
        )
        self.db.commit()
        return self.get(patient_id)
    
    def delete(self, patient_id: int) -> bool:
        if self.get(patient_id) is None:
            return False
        
        self.db.execute(
            text("DELETE FROM patients WHERE id= :id"),
            {"id": patient_id}
        )
        self.db.commit()
        return True
