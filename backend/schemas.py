from pydantic import BaseModel, ConfigDict

# Схема для приема данных от клиента (прием решения кода)
class SubmissionCreate(BaseModel):
    input_code: str
    problem_id: int
    notes: str | None = None
    # ID пользователя будет браться из токена авторизации,
    # а время и статус (PENDING) база проставит сама.

    model_config = ConfigDict(from_attributes=True)

class SubmissionResponse(BaseModel):
    id: int
    status: str
    speed: int | None = None
    memory: int | None = None
    notes: str | None = None
    # строка ниже делает так, что Pydantic понимает объекты SQLAlchemy

    model_config = ConfigDict(from_attributes=True)

class ProblemResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    difficulty: str

    model_config = ConfigDict(from_attributes=True)

class ProblemCreate(BaseModel):
    # ID создается базой данных самостоятельно
    title: str
    description: str | None = None
    difficulty: str
    topic_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

class ProblemDashboard(BaseModel):
    id: int
    title: str
    difficulty: str

    model_config = ConfigDict(from_attributes=True)


class TopicDashboardResponse(BaseModel):
    id: int
    name: str
    problem: list[ProblemDashboard]

    model_config = ConfigDict(from_attributes=True)

#TODO ручки(и схемы) для входа препода и студента должны быть разными, и схемы для них тоже,
# ибо схема на вход студента будет учитывать group_id, а регистрация препода нет.