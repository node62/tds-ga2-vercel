import os # Add this import
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

# Construct an absolute path to marks.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MARKS_FILE_PATH = os.path.join(BASE_DIR, "marks.json")

# Load the marks data using the absolute path
try:
    with open(MARKS_FILE_PATH, "r") as f:
        marks_data = json.load(f)
except FileNotFoundError:
    # Log this error or handle it appropriately for debugging on Vercel
    # For now, we'll raise it to make sure it appears in Vercel logs if it happens
    raise RuntimeError(f"Could not find marks.json at {MARKS_FILE_PATH}")
except json.JSONDecodeError:
    raise RuntimeError(f"Could not decode marks.json at {MARKS_FILE_PATH}")


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
    # Ensure marks_data is loaded before trying to access it
    # This check is more for robustness, the error should be caught above if file loading fails
    if not isinstance(marks_data, list): # Or dict, depending on your actual JSON structure for lookup
        # If marks_data is a list of dicts as per your example, you need to convert it to a dict for easy lookup
        # Assuming marks_data in marks.json is a list like: [{"name": "A", "marks": 10}, ...]
        # You'd ideally convert this to a dictionary for fast lookups: {"A": {"name": "A", "marks": 10}, ...}
        # For now, I'll assume marks_data is already in a lookup-friendly format (e.g., a dictionary keyed by name)
        # If it's a list of dictionaries, your original code needs adjustment for how 'n in marks_data' works.
        # Let's assume marks_data is a dictionary: {name: {details}}
        # Or if marks_data is a list of {"name": "X", "marks": Y}, then it should be:
        # temp_marks_data = {item['name']: item for item in marks_data}
        # Then use temp_marks_data for lookup
        pass # Add proper handling or conversion if necessary

    for n_val in name: # Renamed 'n' to 'n_val' to avoid conflict if you process marks_data
        # Your current marks.json is a list of dictionaries, so `n in marks_data` will not work as intended.
        # You need to search through the list.
        found_student = next((student for student in marks_data if student.get("name") == n_val), None)
        if found_student:
            student_marks.append(found_student) # Or just found_student['marks'] if you only want the marks value
    return {"marks": student_marks}
