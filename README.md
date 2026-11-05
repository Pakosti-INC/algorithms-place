# algorithms-place
## создание venv
> py -m venv .venv 
> venv\Scripts\activate

## установка зависимостей  
> pip install -r requirements.txt

## запуск тестового сервера
> py backend/main.py

## запуск редиса и селери в докере
> docker run -d -p 6379:6379 --name redis_broker redis:alpine
> celery -A worker.celery_app worker --loglevel=info --pool=solo

## Базовый user-flow
> clck.ru/3W3rwC




