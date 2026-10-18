import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from dependencies import get_db, get_current_user
from schemas import *
from sqlalchemy.orm import Session, contains_eager
from models import Submission, Problem, User, GroupProblemLink, Topic
from sqlalchemy import select, exists
from security import get_password_hash, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

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
    return new_problem


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


@app.post("/problems/link", response_model=GroupProblemLinkCreate, status_code=status.HTTP_201_CREATED, tags=["Проблемы"])
def link_problem_to_group(item: GroupProblemLinkCreate, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    if current_user.role == "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе."
        )
    stmt = (select(GroupProblemLink).where(GroupProblemLink.group_id == item.group_id,
                                           GroupProblemLink.problem_id == item.problem_id))
    existing_link = db.scalar(stmt)
    if not existing_link:
        new_link = GroupProblemLink(
            group_id=item.group_id,
            problem_id=item.problem_id,
            deadline=item.deadline
        )
        db.add(new_link)
        db.commit()
        db.refresh(new_link)
        return new_link
    else:
        existing_link.deadline = item.deadline
        db.commit()
        db.refresh(existing_link)
        return existing_link


@app.post("/auth/register", status_code=status.HTTP_201_CREATED, response_model=RegisterNewUserResponse, tags=["Auth"])
def create_new_user(user_data: RegisterNewUser, db: Session = Depends(get_db)):
    stmt = select(exists().where(User.email == user_data.email))
    is_exists = db.scalar(stmt)
    if is_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже зарегистрирован."
        )
    else:
        hash_pass = get_password_hash(user_data.password)

        new_user = User(
            email=user_data.email,
            group_id=user_data.group_id,
            password_hash=hash_pass,
            first_name=user_data.first_name,
            middle_name=user_data.middle_name,
            last_name=user_data.last_name,
            role="STUDENT"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@app.post("/auth/login", status_code=status.HTTP_202_ACCEPTED, response_model=TokenResponse, tags=["Auth"])
def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    stmt = select(User).where(User.email == form_data.username)
    user = db.scalar(stmt)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь ещё не зарегистрирован."
        )
    else:

        is_pass_correct = verify_password(form_data.password, user.password_hash)
        if is_pass_correct:
            payload = {
                "sub": str(user.id),
                "role": user.role,
                "group_id": user.group_id
            }
            access_token = create_access_token(payload)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль"
            )




if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
