import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from dependencies import get_db, get_current_user
from schemas import *
from sqlalchemy.orm import Session, contains_eager
from models import Submission, Problem, User, GroupProblemLink, Topic
from sqlalchemy import select

app = FastAPI()

@app.get("/")
def status_check():
    return {"status": "API is online"}

@app.get("/submissions/my", response_model=list[SubmissionResponse], tags=["Решения"])
def get_my_submissions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Submission).where(Submission.user_id == current_user.id)

    submissions = db.scalars(stmt).all()

    return submissions

@app.get("/submissions/{id}", response_model=SubmissionResponse, tags=["Решения"])
def get_single_submission(id: int, db: Session = Depends(get_db)):
    stmt = select(Submission).where(Submission.id == id)

    submission = db.scalar(stmt)
    if not submission:
        raise HTTPException(status_code=404, detail="Решение не найдено")

    return submission


@app.post("/submissions", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED, tags=["Решения"])
def create_submission(item: SubmissionCreate, db: Session = Depends(get_db)):
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

@app.get("/problems/{id}", response_model=ProblemResponse, tags=["Проблемы"])
def get_single_problem(id: int, db: Session = Depends(get_db)):
    stmt = select(Problem).where(Problem.id == id)

    problem = db.scalar(stmt)
    if not problem:
        raise HTTPException(status_code=404, detail="Проблема не найдена")

    return problem


@app.get("/problems", response_model=list[ProblemResponse], tags=["Проблемы"])
def get_problems(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    stmt = select(Problem).join(GroupProblemLink).where(GroupProblemLink.group_id == current_user.group_id)
    problem = db.scalars(stmt).all()
    return problem

@app.post("/problems/create", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED, tags=["Проблемы"])
def create_problem(item: ProblemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role == "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе."
        )

    new_problem = Problem(
        title=item.title,
       description=item.description,
       difficulty=item.difficulty,
        topic_id=item.topic_id
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return  new_problem

@app.get("/index")
def index():
    return "Типо главная"


@app.get("/dashboard", response_model=list[TopicDashboardResponse], tags=["Дашборд"])
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = (
        select(Topic)
        .join(Topic.problem)
        .join(GroupProblemLink, GroupProblemLink.problem_id == Problem.id)
        .where(GroupProblemLink.group_id == current_user.group_id)
        # Указываем SQLAlchemy упаковать отфильтрованные задачи внутрь тем
        .options(contains_eager(Topic.problem))
    )

    # Вызов .unique() обязателен при джоине связей один-ко-многим,
    # чтобы темы не дублировались в итоговом списке
    topics = db.scalars(stmt).unique().all()

    return topics

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
