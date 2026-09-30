from pydantic import BaseModel, ConfigDict

# Схема для приема данных от клиента (прием решения кода)
class SubmissionCreate(BaseModel):
    input_code: str
    problem_id: int
    notes: str | None = None
    # ID пользователя будет браться из токена авторизации,
    # а время и статус (PENDING) база проставит сама.

class SubmissionResponse(BaseModel):
    id: int
    status: str
    speed: int | None = None
    memory: int | None = None
    notes: str | None = None
    # строка ниже делает так, что Pydantic понимает объекты SQLAlchemy
    model_config = ConfigDict(from_attributes=True)