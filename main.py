import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI(title="AI Interviewer API")

# Enable CORS for Vercel/Frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnswerRequest(BaseModel):
    transcript: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Interview Assistant Backend is Running"}

@app.post("/interview")
def evaluate_interview(request: AnswerRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in environment variables.")

    try:
        client = genai.Client(api_key=api_key)
        
                prompt = (
            "You are a warm, supportive, and friendly AI Interviewer for a university Lecturer position. "
            "Evaluate the candidate's spoken answer below in real-time.\n\n"
            "Format your response EXACTLY like this (do not use markdown formatting):\n"
            "Feedback: [Provide 2 brief, highly encouraging sentences evaluating their answer. Be kind, constructive, and friendly.]\n"
            "Scores - Confidence: [1-10], Technical: [1-10], Communication: [1-10]\n"
            "Next Question: [Ask the next interview question nicely]\n\n"
            f"Candidate's Answer:\n\"{request.transcript}\""
        )

        

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
