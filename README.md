# algorithms-place
## создание venv
> py -m venv .venv 
> venv\Scripts\activate

## установка зависимостей  
> pip install -r requirements.txt

## запуск тестового сервера
> python -m backend.main

## запуск редиса и селери в докере
> docker compose up -d
> 
> (В консоль из папки cd backend) celery -A backend.worker.celery_app worker --loglevel=info --pool=solo

## Базовый user-flow
> clck.ru/3W3rwC




