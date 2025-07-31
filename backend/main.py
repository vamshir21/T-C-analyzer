from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model import analyze_text, tag_risks

app = FastAPI()

# Allow CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

class FeedbackRequest(BaseModel):
    text: str
    summary: str
    rating: str


@app.post("/analyze/")
def analyze(request: AnalyzeRequest):
    try:
        # 🔹 Try to generate the summary
        summary = analyze_text(request.text)

        # 🔹 Detect risks in the summary
        risks = tag_risks(summary)

        return {
            "summary": summary,
            "risks": risks
        }

    except Exception as e:
        # 🔹 Catch and handle any crashes (GPU OOM, index error, etc.)
        print(f"❌ Error in /analyze/: {e}")
        return {
            "summary": "⚠️ Error: Could not process the Terms & Conditions due to an internal issue.",
            "risks": []
        }


@app.post("/feedback/")
def feedback(request: FeedbackRequest):
    # Placeholder: Just log feedback for now
    print(f"Feedback received: {request.rating} for summary:\n{request.summary[:100]}...")
    return {"status": "success"}
