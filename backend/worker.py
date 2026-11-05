
from celery import Celery
import docker
import tempfile
import os
import requests
from backend.database import Session
from backend.models import Submission
from sqlalchemy import select


docker_client = docker.from_env()


def run_code_in_sandbox(input_code: str) -> dict:
    # Создаем временную папку на хосте
    with tempfile.TemporaryDirectory() as temp_dir:
        # Собираем путь к нашему будущему файлу
        file_path = os.path.join(temp_dir, "main.py")

        # Создаем файл и записываем в него код
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(input_code)

        print(f"Временная папка создана здесь: {temp_dir}")
        print(f"Файл main.py готов к пробросу в Docker.")

        container = docker_client.containers.run(
            "python:3.11-alpine", command=["python", "/app/main.py"],
            volumes={temp_dir: {'bind': '/app', 'mode': 'ro'}},
            detach=True, network_disabled=True, mem_limit="128m")
        try:
            result = container.wait(timeout=2)
            output = container.logs().decode("utf-8")

            if result.get("StatusCode") == 0:
                return {"status": "OK", "output": output}
            else:
                return {"status": "RE", "output": output}

        except requests.exceptions.ReadTimeout:
            container.stop()
            return {"status": "TLE", "output": ""}

        finally:
            container.remove(force=True)





# Инициализируем приложение Celery, подключаемся к локальному Redis
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)



@celery_app.task
def process_submission_dummy(submission_id: int):
    with Session() as db:
        stmt = select(Submission).where(Submission.id == submission_id)
        db_submission = db.scalar(stmt)

        if not db_submission:
            print(f"Сабмишен {submission_id} не найден в БД. Пропускаем.")
            return

        input_code = db_submission.input_code

        result = run_code_in_sandbox(input_code)
        db_submission.status = result.get("status")
        db_submission.output = result.get("output")

        db.commit()