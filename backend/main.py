from http.client import HTTPException

import uvicorn
from fastapi import FastAPI, Depends
from database import get_db
from schemas import SubmissionCreate, SubmissionResponse
from sqlalchemy.orm import Session
from models import Submission
from sqlalchemy import select

app = FastAPI()


@app.get("/submissions/{id}", response_model=SubmissionResponse)
def get_submissions(id: int, db: Session = Depends(get_db)):
    stmt = select(Submission).where(Submission.id == id)

    submission = db.scalar(stmt)
    if not submission:
        raise HTTPException(status_code=404, detail="Решение не найдено")

    return submission


@app.post("/submissions", response_model=SubmissionResponse)
def add_submission(item: SubmissionCreate, db: Session = Depends(get_db)):
    new_submission = Submission(
        input_code=item.input_code,
        problem_id=item.problem_id,
        notes=item.notes,
        user_id=1
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission



if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)