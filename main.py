import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# Load the marks data from the JSON file
# This will be loaded once when the application starts
try:
    with open("marks.json", "r") as f:
        students_data = json.load(f)
except FileNotFoundError:
    students_data = [] # Handle case where file might not be found, though it should be deployed
except json.JSONDecodeError:
    students_data = [] # Handle case where JSON is invalid

# Create a dictionary for faster lookups
marks_dict = {student["name"]: student["marks"] for student in students_data}

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Allows only GET requests
    allow_headers=["*"],  # Allows all headers
)

@app.get("/api")
async def get_marks(names: List[str] = Query(None, alias="name")):
    """
    Retrieves the marks for the given list of student names.
    Example: /api?name=X&name=Y
    """
    results = []
    if names:
        for name in names:
            # Get marks from the pre-loaded dictionary
            mark = marks_dict.get(name)
            # The problem asks for marks of X and Y in the same order.
            # If a name is not found, its mark is not added to the list,
            # as per the example output { "marks": [10, 20] }
            if mark is not None:
                results.append(mark)
            # If you need to explicitly return null or an indicator for not found:
            # else:
            # results.append(None) # Or some other placeholder

    return {"marks": results}

# Optional: A root endpoint for basic testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the Marks API. Use /api?name=STUDENT_NAME to get marks."}