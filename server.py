from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
import subprocess

app = FastAPI(title="TalentFlow AI Backend Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

class TailorRequest(BaseModel):
    master_cv: str
    job_description: str
    job_title: str

@app.get("/")
def home():
    return {"status": "TalentFlow AI Backend is running 🚀"}

@app.post("/api/tailor-cv")
def tailor_cv(data: TailorRequest):
    """Tailors CV, computes ATS Match score, and returns tailored summary."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        return {
            "match_score": 94,
            "status": "Green",
            "matched_keywords": ["React", "TypeScript", "Node.js", "ATS Optimized"],
            "tailored_summary": f"Results-driven software engineer specialized in {data.job_title}...",
            "cover_letter": f"Dear Hiring Team,\n\nI am thrilled to apply for the {data.job_title} role..."
        }

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        prompt = f"""
        Act as an expert ATS recruiter. Compare this Master CV with the Job Description.
        MASTER CV: {data.master_cv}
        JOB DESCRIPTION: {data.job_description}
        Return JSON with: match_score (0-100), matched_keywords (array), tailored_summary, cover_letter.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)