from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import analyze_text, tag_risks

app = FastAPI()

# Enable CORS for local extension use only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/analyze/")
def analyze(request: TextRequest):
    summary = analyze_text(request.text)
    risks = tag_risks(summary)
    return {"summary": summary, "risks": risks}
