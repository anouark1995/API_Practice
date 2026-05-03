from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.grade import GradeCreate, GradeUpdate


class GradeService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[dict]:
        # TODO: query all rows from the `grades` table
        # Hint: look at how StudentService.list_all() does it with text()
        # Return a list of dicts with keys: id, score, label, student_id
        rows = self.db.execute(text("SELECT id, score, label, student_id FROM grades")).fetchall()
        return [{"id": r.id, "score": r.score, "label": r.label, "student_id": r.student_id} for r in rows]

    def get(self, grade_id: int) -> dict | None:
        # TODO: query a single grade by its id
        # Hint: use a WHERE id = :id clause, same pattern as StudentService.get()
        # Return None if the row doesn't exist
        row = self.db.execute(
            text("SELECT id, score, label, student_id FROM grades WHERE id = :id"),
            {"id":grade_id},
        ).fetchone()
        if row is None:
            return None
        return {"id": row.id, "score": row.score, "label": row.label, "student_id": row.student_id}
    
    def grade_exists(self, id: int)-> bool:
        grade = self.db.execute(
            text("SELECT id from grades where id = :id"),
            {"id": id},
        ).fetchone()

        if grade is None:
            return False
        return True

    def create(self, data: GradeCreate) -> dict | None:
        # TODO: before inserting, check that the student_id actually exists in the `students` table
        # If the student doesn't exist, return None (the route will turn that into a 400)
        student = self.db.execute(
            text("SELECT id FROM students WHERE id = :id"),
            {"id": data.student_id},
        ).fetchone()

        if student is None:
            return None
        
        result = self.db.execute(
            text("INSERT INTO grades (score, label, student_id) VALUES (:score, :label, :student_id)"),
            {"score": data.score, "label": data.label, "student_id": data.student_id},
        )
        self.db.commit()
        return self.get(result.lastrowid)
        # Then INSERT into `grades` and return the newly created grade via self.get()
        # Don't forget to commit!
        

    def update(self, grade_id: int, data: GradeUpdate) -> dict | None:
        # TODO: check the grade exists first (return None → 404 if not)
        if not self.grade_exists(grade_id):
            return None
        
        # Build a dynamic SET clause from data.model_dump(exclude_unset=True)
        # If student_id is being changed, verify the new student exists
        # Execute the UPDATE, commit, and return the updated grade via self.get()
        self.db.execute(
            text(f"UPDATE students SET {set_clause} WHERE id = :id"),
            fields,
        )
        self.db.commit()
        return self.get(student_id)
        return None

    def delete(self, grade_id: int) -> bool:
        # TODO: check the grade exists first (return False → 404 if not)
        
        if not self.grade_exists(grade_id):
            return False
        
        # Execute DELETE FROM grades WHERE id = :id, commit, and return True
        self.db.execute(
            text("DELETE FROM grades WHERE id = :id"),
             {"id": grade_id},
        )

        self.db.commit()
        return True
