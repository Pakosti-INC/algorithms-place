from sqlalchemy import Integer, String, Text, Enum, ForeignKey, Boolean, func
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.orm import relationship
import enum


Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    invite_code: Mapped[str] = mapped_column(String(16), unique=True)

    # relationship для получения всех студентов группы (group.users)
    users: Mapped[list["User"]] = relationship(back_populates="group")

class UsersRole(str, enum.Enum):
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
    MODERATOR = "MODERATOR"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(60), unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    middle_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30))
    role: Mapped[UsersRole] = mapped_column(default=UsersRole.STUDENT)
    #TODO Не забыть про добавление соли к хэшу!
    password_hash: Mapped[str] = mapped_column(Text)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)

    # relationship для получения группы студента (user.group)
    group: Mapped["Group"] = relationship(back_populates="users")

class Problem(Base):
    __tablename__ = 'problems'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(30))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))

    # relationship для получения всех тестов у проблемы (problem.tests)
    tests: Mapped[list["Test"]] = relationship(back_populates="problem")
    # relationship для получения темы у проблемы (problem.topic)
    topic: Mapped[list["Topic"]] = relationship(back_populates="problem")


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    input_data: Mapped[str] = mapped_column(Text)
    output_data: Mapped[str] = mapped_column(Text)
    is_hidden: Mapped[bool] = mapped_column(Boolean)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

    # relationship для получения всех проблем у  (problem.tests)
    problem: Mapped["Problem"] = relationship(back_populates="tests")

class SubmissionStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    WA = "WRONG ANSWER"
    TO = "TIMEOUT"

class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    input_code: Mapped[str] = mapped_column(Text)
    status: Mapped[SubmissionStatus] = mapped_column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING)
    # Пока не будет выбора ЯП.
    #code_lang: Mapped[#SubmissionLangSelect] = mapped_column(Enum(SubmissionLangSelect))
    send_time: Mapped[datetime] = mapped_column(server_default=func.now())
    speed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Скорость решения задачи в мс")
    memory: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Память затраченная сервером на решение задачи в килобайтах")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

class ReviewStatus(enum.Enum):
    ACCEPTED = "Accepted"
    INCORRECT = "Incorrect"

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer , primary_key=True)
    status: Mapped[ReviewStatus] = mapped_column()
    comment: Mapped[str] = mapped_column(Text)
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer , primary_key=True)
    name: Mapped[str] = mapped_column(Text)

    problem: Mapped[list["Problem"]] = relationship(back_populates="topic")


