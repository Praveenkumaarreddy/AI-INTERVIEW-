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
            "You are a professional, strict yet encouraging panel interviewer evaluating a candidate "
            "for an English Lecturer position. Evaluate their answer considering communication skills, "
            "clarity, confidence, and pedagogy.\n\n"
            f"Candidate's Spoken Answer:\n\"{request.transcript}\"\n\n"
            "Provide brief, constructive feedback (3-4 sentences max) and end with the next interview question."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
