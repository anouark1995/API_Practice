from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.grade import GradeCreate, GradeOut, GradeUpdate
from app.services.grade_service import GradeService

router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("", response_model=list[GradeOut])
def list_grades(db: Session = Depends(get_db)):
    # TODO: call GradeService(db).list_all() and return the result
    return GradeService(db).list_all()


@router.get("/{grade_id}", response_model=GradeOut)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    # TODO: call GradeService(db).get(grade_id)
    grade= GradeService(db).get(grade_id)
    # If the result is None, raise a 404 HTTPException with detail "Grade not found"
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    # Otherwise return the grade
    return grade


@router.post("", response_model=GradeOut, status_code=status.HTTP_201_CREATED)
def create_grade(data: GradeCreate, db: Session = Depends(get_db)):
    grade = GradeService(db).create(data)
    if grade is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student does not exist")
    return grade
    


@router.patch("/{grade_id}", response_model=GradeOut)
def update_grade(grade_id: int, data: GradeUpdate, db: Session = Depends(get_db)):
    # TODO: call GradeService(db).update(grade_id, data)
    grade = GradeService(db).update(grade_id,data)
    # If the result is None, raise 404 "Grade or student not found"
    # Otherwise return the updated grade
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade or student not found")
    return grade


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    # TODO: call GradeService(db).delete(grade_id)
    # If it returns False, raise 404 "Grade not found"
    if not GradeService(db).delete(grade_id):
        raise HTTPException(status_code = 404, detail = "Grade not found")
    # If it returns True, just return None (FastAPI handles the 204 response)
    return None
