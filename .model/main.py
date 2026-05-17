from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import date
from ml import predict_patient

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
supabase = create_client(
    os.getenv('EXPO_PUBLIC_SUPABASE_URL'),
    os.getenv('EXPO_PUBLIC_SUPABASE_PUBLISHABLE_KEY')
)

@app.get("/")
def index():
    return {"message": "Running!"}

@app.get("/calculate")
def calculate_friends(id):
    response = supabase.table("patient").select("dob, sBP, dBP, bloodSugar, heartRate").eq("id", id).execute()
    first_record = response[0]

    dob = date.fromisoformat(first_record["dob"])
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    prediction = predict_patient(age, first_record["sBP"], first_record["dBP"], first_record["bloodSugar"], first_record["heartRate"])
    return {
        "sBP": first_record["sBP"],
        "dBP": first_record["dBP"],
        "bloodSugar": first_record["bloodSugar"],
        "heartRate": first_record["heartRate"],
        "prediction": prediction
    }


@app.get("/friends")
def get_friends(id):
    response = supabase.table("friends").select("friendID, loginDetails(firstName, lastName)").eq("id", id).execute()

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
        ids_list.append(f"id.eq.{item}")
    
    board_ids = ",".join(ids_list)
    response = supabase.table("leaderboard").select("points, loginDetails(firstName, lastName)").or_(board_ids).execute()
    result = []
    for item in response.data:
        first_name = item["loginDetails"]["firstName"]
        last_initial = item["loginDetails"]["lastName"][0]
        points = int(item["points"])
        result.append({"name": f"{first_name} {last_initial}.", "points": points})
    
    result = sorted(result, key=lambda x: x["points"], reverse=True)
    for i in range(len(result)):
        result[i]["rank"] = i
    
    return result