
from celery import Celery
from backend.database import Session
from backend.models import Submission, Test
from sqlalchemy import select
from backend.sandbox import run_test_in_docker
import re

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

        stmt_test = select(Test).where(Test.problem_id == db_submission.problem_id)
        # Добавляем .all(), чтобы вытащить тесты в список
        test_cases = db.scalars(stmt_test).all()

        if not test_cases:
            print(f"Проблема {db_submission.problem_id} не содержит тестов")
            db_submission.status = "ERROR"
            db.commit()
            return
        max_time_ms = 0
        max_memory_mb = 0.0
        input_code = db_submission.input_code


        for test in test_cases:
            exit_code, output_str, time_output = run_test_in_docker(submission_id=submission_id, input_code=input_code, data=test.input_data)
            db_submission.output = output_str
            if exit_code == 124:
                db_submission.status = "Time Limit Exception"
                db.commit()
                return

            elif exit_code != 0:
                db_submission.status = "Runtime Error"
                db.commit()
                return

            elif output_str.strip() != test.output_data.strip():
                db_submission.status = "Wrong Answer"
                db.commit()
                return

        # Парсим User time (в секундах переводим в миллисекунды)
        time_match = re.search(r"User time \(seconds\):\s*([\d.]+)", time_output)
        if time_match:
            sec = float(time_match.group(1))
            ms = float(sec * 1000)
            max_time_ms = max(max_time_ms, ms)

        # Парсим Maximum resident set size (в килобайтах переводим в мегабайты)
        mem_match = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", time_output)
        if mem_match:
            kb = int(mem_match.group(1))
            mb = round(kb / 1024, 2)
            max_memory_mb = max(max_memory_mb, mb)

        db_submission.memory = f"{max_memory_mb} MB"
        # Сохраняем в базу
        db_submission.speed = f"{max_time_ms} ms"
        db_submission.status = "ACCEPTED"
        db.commit()
        return