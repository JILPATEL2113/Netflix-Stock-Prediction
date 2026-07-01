import pickle
import os  # <-- Environment variables read karne ke liye
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv  # <-- dotenv import karein

# 🔥 .env file ke variables ko load karein
load_dotenv()

app = FastAPI(title="Netflix Stock Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model load karne ka logic
try:
    with open('netflix_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
except FileNotFoundError:
    print("❌ Error: netflix_model.pkl file nahi mili!")

class StockInput(BaseModel):
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float

@app.get("/")
def home():
    return {"message": "Welcome to Netflix Stock Prediction API!"}

@app.post("/predict")
def predict_stock(data: StockInput):
    try:
        input_features = np.array([[data.Open, data.High, data.Low, data.Close, data.Volume]])
        prediction = loaded_model.predict(input_features)[0]
        return {
            "status": "success",
            "predicted_tomorrow_close": round(float(prediction), 2)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 🔥 Agar aap direct python app.py chalao toh .env se port uthaye
if __name__ == "__main__":
    import uvicorn
    # .env se HOST aur PORT nikalna, nahi toh default set karna
    server_host = os.getenv("HOST", "127.0.0.1")
    server_port = int(os.getenv("PORT", 8000))
    
    uvicorn.run("app:app", host=server_host, port=server_port, reload=True)