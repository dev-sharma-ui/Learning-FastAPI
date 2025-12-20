from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {"Hello World!..."}

@app.get('/homepage')
def homepage():
    return "HomePage"


@app.get('/homepage/{id}')
def passid(id: int):
    return {"ID:", id}
