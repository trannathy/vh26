from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from datetime import date
from ml import predict_patient

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

class BPLog(BaseModel):
    systolic: int
    diastolic: int

class HRLog(BaseModel):
    bpm: int

class BSLog(BaseModel):
    bloodSugar: float

@app.get("/")
def index():
    return {"message": "Running!"}

@app.get("/calculate")
def calculate_friends(id):
    response = supabase.table("patient").select("dob, sBP, dBP, bloodSugar, heartRate").eq("id", id).execute()
    first_record = response.data[0]

    dob = date.fromisoformat(first_record["dob"])
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    prediction = predict_patient(age, int(first_record["sBP"][0]), int(first_record["dBP"][0]), int(first_record["bloodSugar"][0]), int(first_record["heartRate"][0]))
    return {
        "sBP": int(first_record["sBP"][0]),
        "dBP": int(first_record["dBP"][0]),
        "bloodSugar": int(first_record["bloodSugar"][0]),
        "heartRate": int(first_record["heartRate"][0]),
        "prediction": prediction
    }


@app.get("/friends")
def get_friends(id):
    response = supabase.table("friends").select("friendID, loginDetails!friends_friendID_fkey(firstName, lastName)").eq("id", id).execute()

    result = []
    for item in response.data:
        first_name = item["loginDetails"]["firstName"]
        first_inital = item["loginDetails"]["firstName"][0]
        last_initial = item["loginDetails"]["lastName"][0]
        result.append({"name": f"{first_name} {last_initial}.", "initials": f"{first_inital}{last_initial}"})
    
    return result

@app.get("/leaderboard")
def get_leaderboard(id):
    response = supabase.table("friends").select("friendID").eq("id", id).execute()
    ids_list = [f"id.eq.{id}"]
    for item in response.data:
        ids_list.append(f"id.eq.{item['friendID']}")
    
    board_ids = ",".join(ids_list)
    response = supabase.table("leaderboard").select("points, loginDetails(firstName, lastName)").or_(board_ids).execute()
    result = []
    for item in response.data:
        first_name = item["loginDetails"]["firstName"]
        last_initial = item["loginDetails"]["lastName"][0]
        points = item["points"]
        result.append({"name": f"{first_name} {last_initial}.", "points": points})
    
    result = sorted(result, key=lambda x: x["points"], reverse=True)
    for i in range(len(result)):
        result[i]["rank"] = i + 1
    
    return result

@app.post("/logBP/{id}")
async def log_bp(id: int, bp: BPLog):
    supabase.table("patient").update({"sBP": [bp.systolic], "dBP": [bp.diastolic]}).eq("id", id).execute()

@app.post("/logHR/{id}")
async def log_hr(id: int, hr: HRLog):
    supabase.table("patient").update({"heartRate": [hr.bpm]}).eq("id", id).execute()

@app.post("/logBS/{id}")
async def log_bs(id: int, bs: BSLog):
    supabase.table("patient").update({"bloodSugar": [bs.bloodSugar]}).eq("id", id).execute()