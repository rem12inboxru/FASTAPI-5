from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async  def get_all(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get("/user/{id}")
async  def users_get(request: Request, id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[id-1]})

@app.post("/user/{username}/{age}")
async def users_post(user: User, username: str, age: int) -> User:
    user.id = len(users) +1
    users.append(user)
    user.username = username
    user.age = age
    return user


@app.put("/user/{id}/{username}/{age}")
async def users_put(user: User, id: int, username: str, age: int) -> User:
    try:
        user.id = id -1
        user = users[user.id]
        user.username = username
        user.age = age
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete('/user/{id}')
async def users_delete(user: User, id: int) -> str:
    try:
        user.id = id -1
        users.pop(user.id)
        return f"User {id} has been deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")

if __name__ == '__main__':
    uvicorn.run(app="CRUD2:app", reload=True)