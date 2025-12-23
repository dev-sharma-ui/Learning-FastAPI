from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "name": "DEV"}
    )

@app.get('/home')
def home(limit: int = 10, parameter: bool = True, sort: Optional[str] = None):
    if parameter:
        return {"Blogs" : f'{limit} is the no. of blog'}
    else:
        return {"Blogs": f'from else block {limit}'}

class Hello(BaseModel):
    firstName : str
    lastName : str
    published: Optional[bool]

@app.post('/blog')
def submit(request: Hello):
    return {f"Fisrt name: {request.firstName}"
            f", Last name: {request.lastName}"}

