import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os # Used for more robust path handling, though not strictly necessary if files are in root

# --- Configuration ---
# Assuming marks.json is in the same directory as main.py
MARKS_FILENAME = "marks.json"

# --- Data Loading ---
students_data = []
marks_dict = {}

try:
    # Get the absolute path to the directory where this script is located
    # This helps in reliably finding marks.json, especially in serverless environments.
    # However, Vercel typically sets the working directory to the root of your project
    # where main.py and marks.json are located.
    # For simplicity and directness with Vercel's usual setup where main.py is at the root:
    with open(MARKS_FILENAME, "r") as f:
        students_data = json.load(f)
    
    # Create a dictionary for faster lookups: {name: marks}
    marks_dict = {student["name"]: student["marks"] for student in students_data}
    print(f"Successfully loaded {len(students_data)} student records from {MARKS_FILENAME}.")

except FileNotFoundError:
    print(f"CRITICAL ERROR: The marks file '{MARKS_FILENAME}' was not found.")
    print(f"Please ensure '{MARKS_FILENAME}' is in the same directory as main.py: {os.getcwd()}")
    # students_data and marks_dict will remain empty
except json.JSONDecodeError:
    print(f"CRITICAL ERROR: Could not decode '{MARKS_FILENAME}'. Ensure it contains valid JSON.")
    # students_data and marks_dict will remain empty
except Exception as e:
    print(f"CRITICAL ERROR: An unexpected error occurred while loading '{MARKS_FILENAME}': {e}")
    # students_data and marks_dict will remain empty


# --- FastAPI Application Setup ---
app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
# This allows web pages from any domain to make GET requests to your API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (websites)
    allow_credentials=True, # Allows cookies or authorization headers if you were using them
    allow_methods=["GET"],  # Specifically allows only GET requests
    allow_headers=["*"],  # Allows all types of headers in the request
)


# --- API Endpoints ---
@app.get("/")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Student Marks API. Use the /api endpoint to query marks."}


@app.get("/api")
async def get_student_marks(names: List[str] = Query(..., alias="name")):
    """
    Retrieves the marks for a list of student names provided as query parameters.
    Example request: /api?name=Alice&name=Bob
    Returns a JSON object with a "marks" key containing a list of marks in the same order.
    If a student name is not found, their mark is not included in the result list.
    """
    found_marks = []
    if not marks_dict:
        print("Warning: Marks dictionary is empty. Was the JSON file loaded correctly?")
        # Depending on desired behavior, you could return an error here or just empty marks.

    if names: # names will be a list of strings passed via ?name=X&name=Y
        for student_name in names:
            mark = marks_dict.get(student_name) # Efficiently look up the mark
            if mark is not None:
                found_marks.append(mark)
            # If student_name is not in marks_dict, mark will be None, and it's skipped.
            # This matches the example output: { "marks": [10, 20] }

    return {"marks": found_marks}

# --- Local Development Runner (Optional) ---
# This block allows you to run the server locally using "python main.py"
# Vercel itself will not use this block; it imports the `app` object directly.
if __name__ == "__main__":
    import uvicorn
    print("Starting local development server with Uvicorn...")
    print(f"Navigate to http://127.0.0.1:8000 in your browser.")
    print(f"Test the API: http://127.0.0.1:8000/api?name=GWME&name=LRIP (replace with actual names)")
    uvicorn.run(app, host="0.0.0.0", port=8000)