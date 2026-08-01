from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

# Initialize FastAPI app
app = FastAPI()

# Allow your Vercel frontend to communicate with this Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Define the expected data format from the frontend
class InterviewRequest(BaseModel):
    transcript: str

# Health check route (to wake up Render and test connection)
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Interview Assistant Backend is Running"}

# Main AI Interview route
@app.post("/interview")
async def process_interview(request: InterviewRequest):
    try:
        # Using the fast model for real-time conversation
            model = genai.GenerativeModel("gemini-1.5-flash")

        
        # The friendly AI prompt with dynamic scoring
        prompt = (
            "You are a warm, supportive, and friendly AI Interviewer for a university Lecturer position. "
            "Evaluate the candidate's spoken answer below in real-time.\n\n"
            "Format your response EXACTLY like this (do not use markdown formatting):\n"
            "Feedback: [Provide 2 brief, highly encouraging sentences evaluating their answer. Be kind, constructive, and friendly.]\n"
            "Scores - Confidence: [1-10], Technical: [1-10], Communication: [1-10]\n"
            "Next Question: [Ask the next interview question nicely]\n\n"
            f"Candidate's Answer:\n\"{request.transcript}\""
        )
        
        response = model.generate_content(prompt)
        
        return {"response": response.text}
        
    except Exception as e:
        print(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze answer with AI.")
