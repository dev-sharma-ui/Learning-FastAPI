from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Annotated, Literal
from pydantic import BaseModel, Field, field_validator, computed_field
import json

app = FastAPI()

class Patient(BaseModel):
    id: str = Field(..., description="ID of the Pateint", examples=["P001","P002","P003"])
    name: str = Field(..., description="Name of the Patient", examples=["Dev","Rahul","Riya"])
    city: str = Field(..., description="City of the patient lives in", examples=["Chandigarh","Jalandhar"])
    age: int = Field(...,le=100, ge=0, description="Age of the Patient", examples=[23,44], strict=True)
    gender: Annotated[Literal['male', 'female', 'Prefer not to say'], Field(..., description="Gender of the Patient", examples=["male","female","prefer not to say"])]
    height: float = Field(..., description = "height of the patient in mtrs",examples = [1.70,1.82])
    weight: float = Field(..., description="weight of the patient in kgs", examples=[55,67,76])


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        else:
            return "Obese"
        

def load_data():
    with open('file.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('file.json', 'w') as f:
        json.dump(data, f)
    

class MessageResponse(BaseModel):
    message: str

@app.post(
    "/create",
    status_code=201,
    response_model=MessageResponse
)
def create(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=409, detail="Patient already exists...") 
    
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Pateint has been created successfully'})




