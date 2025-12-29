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
        

class PatientUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    height: Optional[float] = Field(default=None)
    weight: Optional[float] = Field(default=None)

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


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    existing_patient_info['id'] = patient_id

    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return {"message" :"Patient Updated Successfully"}

