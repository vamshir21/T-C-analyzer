# 🔍 T&C Analyzer — Chrome Extension + AI Backend

Automatically extract and summarize complex **Terms and Conditions** using AI.  
Built with a FastAPI backend + Chrome extension frontend for ease of use.

---

## 🚀 Features

- 🧠 **AI-Powered Summarization** using Transformer models (`BART`, `DistilBART`, etc.)
- ⚠️ **Risk Tagging** — Highlights clauses like data sharing, tracking, no refunds, etc.
- 💡 **Click-to-Summarize** — Users highlight text manually before summarizing
- ⚙️ **Chrome Extension** to run directly on any webpage
- 🛡️ Built for future upgrades like reverse image search, credibility scoring, etc.

---

## 🧩 Project Structure

T-C-analyzer/
├── backend/ # FastAPI backend with transformer model
│ ├── model.py # Summarization logic, text cleaner, tagger
│ ├── main.py # FastAPI server
│ └── requirements.txt # Python dependencies
├── extension/ # Chrome extension frontend
│ ├── popup.html
│ ├── popup.js
│ ├── content.js
│ ├── background.js
│ └── manifest.json
└── README.md # Project documentation
## 🛠️ Installation

### Backend (Python + FastAPI)

1. Clone the repo:
   
   git clone https://github.com/vamshir21/T-C-analyzer.git
   cd T-C-analyzer/backend

Create virtual environment:
python -m venv myenv
myenv\Scripts\activate   # On Windows

Install dependencies:
pip install -r requirements.txt

Run FastAPI server:
uvicorn main:app --reload

Chrome Extension
Go to chrome://extensions/
Enable Developer Mode
Click Load Unpacked
Select the /extension folder

🧪 Usage
Open any Terms & Conditions page

Highlight the relevant section of text

Click the Summarize button in the extension

View AI summary and risk tags instantly

📌 To-Do (Planned Features)
 Add UI-based risk highlights

 Support deepfake image detection

 Add source credibility scoring

 Allow saving summaries to cloud

 Option to fine-tune model on legal data

🤖 Model Info
Using facebook/bart-large-cnn for high-quality summarization.
Supports long-form text split into chunks before processing.

📄 License
MIT License © 2025 Vamshi R. Yadav

