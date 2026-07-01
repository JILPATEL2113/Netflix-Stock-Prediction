# 1. Base Python image use karein
FROM python:3.11-slim

# 2. Container ke andar 'app' naam ka working directory banayein
WORKDIR /app

# 3. Sabse pehle requirements file ko container mein copy karein
COPY requirements.txt .

# 4. Saari zaroori Python libraries install karein
RUN pip install --no-cache-dir -r requirements.txt

# 5. Baaki bacha saara code aur model file container mein copy karein
# (Isme aapka app.py aur netflix_model.pkl dono chale jayenge)
COPY . .

# 6. Container ka port 8000 open karein kyunki FastAPI wahan chalta hai
EXPOSE 8000

# 7. Command jo container start hote hi FastAPI server ko run karegi
# (Baaki saari upar ki lines same rahengi, bas aakhiri CMD line ko badlein)
CMD ["python", "app.py"]