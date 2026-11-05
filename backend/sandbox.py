import docker
import tempfile
import os
import requests


client = docker.from_env()

test_code = 'print("Hello from Docker!")'

# Создаем временную папку на хосте
with tempfile.TemporaryDirectory() as temp_dir:
    # Собираем путь к нашему будущему файлу
    file_path = os.path.join(temp_dir, "main.py")

    # Создаем файл и записываем в него код
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(test_code)

    print(f"Временная папка создана здесь: {temp_dir}")
    print(f"Файл main.py готов к пробросу в Docker.")

    container = client.containers.run(
        "python:3.11-alpine", command=["python", "/app/main.py"],
        volumes={temp_dir: {'bind': '/app', 'mode': 'ro'}},
        detach=True, network_disabled=True, mem_limit="128m")
    try:
        # Ждем максимум 2 секунды
        result = container.wait(timeout=2)
        # Если код успел выполниться, забираем логи и декодируем байты в строку
        output = container.logs().decode("utf-8")
        print(f"Статус: OK\nВывод: {output}")

    except requests.exceptions.ReadTimeout:
        # Если время вышло, останавливаем контейнер
        container.stop()
        print("Статус: Time Limit Exceeded (TLE)")

    finally:
        # Гарантированно удаляем контейнер из системы при любом исходе
        container.remove(force=True)


# Как только код доходит сюда, папка temp_dir и файл main.py навсегда удаляются ОС
print("Скрипт завершен, мусор убран.")