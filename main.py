from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

# Load the marks data (replace with your actual data loading)
with open("marks.json", "r") as f:
    marks_data = json.load(f)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api")
async def get_marks(name: list[str] = Query(...)):
    student_marks = []
    for n in name:
        if n in marks_data:
            student_marks.append(marks_data[n])
    return {"marks": student_marks}
