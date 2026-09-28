import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Пришли с пустыми руками (GET) -> Просим выдать список
@app.get("/problems")
def get_problems():
    return [{"title": "Бинарный поиск"}]



if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)