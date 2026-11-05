import time
from celery import Celery

# Инициализируем приложение Celery, подключаемся к локальному Redis
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_submission_dummy(submission_id: int):
    print(f"[{submission_id}] Задача взята в работу. Имитация запуска песочницы...")
    time.sleep(5)
    print(f"[{submission_id}] Имитация завершена. Тут будет обновление статуса в БД.")
    return "OK"