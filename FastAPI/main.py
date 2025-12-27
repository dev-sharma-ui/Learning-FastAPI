from fastapi import FastAPI, Request, Path, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import json


app = FastAPI()

def load_data():
    with open('file.json', 'r') as f:
        data = json.load(f)
    return data


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
    return {
                "Fisrt name: ": request.firstName,
                "Last name: ": request.lastName
           }



@app.get('/comments')
def comments(three: int = 3):
    return f"There are {three} comments"



class project(BaseModel):
    name: str = Field(..., min_length=3, description="User Name", examples=["Dev Sharma"])
    id: int
    is_male: Optional[bool] = True

@app.post('/project')
def small_project(request: project):
    return {
        "UserName: ": request.name,
        "UserID: ": request.id,
        "Is_Male: ": request.is_male
    }


@app.get('/view')
def view_data():
    data = load_data()
    return data

@app.get('/patients/{id}')
def patients(id : str):
    data = load_data()
    if id in data:
        return data[id]
    raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
                  order: str = Query('asc', description="Sort in asc or desc order")):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid Field Select from {valid_fields}")
     
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid Order, Select between asc or desc")
    
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)

    return sorted_data

