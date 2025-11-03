from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated,Optional
import pickle
import pandas as pd
import os
import xgboost as xgb
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_VERSION='1.0.0'

@app.get('/')
def home():
    return{'message':"Insurance API"}

@app.get('/health')
def health_check():
    return{
        'status':'OK',
        'version': MODEL_VERSION
    }


#import the ml model
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'insurance_model.json')
model = xgb.XGBRegressor()
model.load_model(model_path)


#validate incoming model
class UserInput(BaseModel):
    name: Optional[str] = Field(None, description="Full name of the user (optional)")
    email: Optional[str] = Field(None, description="Email address (optional)")
    phone: Optional[str] = Field(None, description="Phone number (optional)")
    age: Annotated[int,Field(...,gt=0,lt=120,description='Age of the user')]
    sex:Annotated[Literal['male','female','others'],Field(...,description='Gender of the user')]
    weight:Annotated[float,Field(...,gt=0,description='Height of the user in meters')]
    height:Annotated[float,Field(...,gt=0,lt=3,description='Weight of the user in kilograms')]
    children:Annotated[int,Field(...,ge=0,description="The number of children the user has.")]
    smoker:Annotated[bool,Field(...,description='Is user a smoker')]
    region:Annotated[Literal['northeast','northwest','southeast','southwest'],Field(...,description='The region user belongs to')]

    @computed_field
    @property
    def age_group(self)->str:
        if self.age <= 12:
            return "kid"
        elif 13 <= self.age <= 19:
            return "teen"
        elif 20 <= self.age <= 44:
            return "adults"
        elif 45 <= self.age <= 59:
            return "middle aged"
        else:
            return "senior"


    @computed_field
    @property
    def sex_encoded(self)->int:
        return 1 if self.sex.lower()=='female' else 0

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi>30:
            return "high"
        elif self.smoker or self.bmi>27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def region_encoded(self) -> list[int]:
        # One-hot encode region for ['northwest', 'southeast', 'southwest']
        regions = ['northwest', 'southeast', 'southwest']
        region_lower = self.region.lower().strip()
        return [1 if region_lower == r else 0 for r in regions]

    @computed_field
    @property
    def bmi_category(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


@app.post("/predict")
def predict_charges(data:UserInput):
    input_df = pd.DataFrame([{
        'age': data.age,
        'sex': data.sex_encoded,
        'bmi': data.bmi,
        'children': data.children,
        'smoker': int(data.smoker),  # convert bool to int if model expects 0/1
        'region_northwest': data.region_encoded[0],
        'region_southeast': data.region_encoded[1],
        'region_southwest': data.region_encoded[2]
    }])

    prediction=model.predict(input_df)[0]

    if prediction < 0 or prediction > 1000000:
        return JSONResponse(status_code=400, content={"error": "Invalid prediction value."})

    save_path = os.path.join(os.path.dirname(__file__), "insurance_predictions.xlsx")

    record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": data.name,
        "Email": data.email,
        "Phone": data.phone,
        "Age": data.age,
        "Sex": data.sex,
        "Weight": data.weight,
        "Height": data.height,
        "BMI": data.bmi,
        "Children": data.children,
        "Smoker": data.smoker,
        "Region": data.region,
        "BMI Category": data.bmi_category,
        "Lifestyle Risk": data.lifestyle_risk,
        "Age Group": data.age_group,
        "Predicted Charges": round(prediction, 2)
    }

    if os.path.exists(save_path):
        existing = pd.read_excel(save_path)
        updated = pd.concat([existing, pd.DataFrame([record])], ignore_index=True)
        updated.to_excel(save_path, index=False)
    else:
        pd.DataFrame([record]).to_excel(save_path, index=False)

    # ✅ Return final result
    result = {
        "predicted_charges": round(float(prediction), 2),
        "bmi": data.bmi,
        "bmi_category": data.bmi_category,
        "lifestyle_risk": data.lifestyle_risk,
        "age_group": data.age_group
    }

    return JSONResponse(status_code=200, content=result)


