from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()


templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "name": "DEV"}
    )




# @app.get('/')
# def home():
#     return {"Hello World!..."}

@app.get('/homepage')
def homepage():
    return "HomePage"


@app.get('/homepage/{id}')
def passid(id: int):
    return {"ID:", id}

@app.get('/homepage/check/{limi}')
def passid(limi: int):
    return {"Limit is: ",limi}


