import torch
from transformers import pipeline

# Auto-select GPU if available
device = 0 if torch.cuda.is_available() else -1
print(f"✅ Using {'GPU' if device == 0 else 'CPU'}")

# Load summarization pipeline
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=device
)

# Risk keywords for tagging
RISK_KEYWORDS = {
    "data sharing": ["share your data", "third parties", "sell your data"],
    "no refunds": ["no refunds", "non-refundable", "cannot return"],
    "tracking": ["cookies", "track your behavior", "analytics tools"],
    "liability": ["not responsible", "no liability", "at your own risk"],
    "arbitration": ["binding arbitration", "waive your right", "no class action"]
}

def split_text(text, max_words=800):
    """Split text into smaller chunks to avoid token overflow."""
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def analyze_text(text: str) -> str:
    """
    Summarize T&C text into 5 structured sections with shorter but detailed summary.
    """
    # 🔹 Step 1: Split into safe chunks
    chunks = split_text(text)

    # 🔹 Step 2: Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        summary = summarizer(
            chunk,
            max_length=200,  # smaller max for each chunk
            min_length=50,
            do_sample=False
        )[0]["summary_text"]
        chunk_summaries.append(summary)

    # 🔹 Step 3: Combine summaries
    raw_summary = " ".join(chunk_summaries)

    # 🔹 Step 4: Structure into sections
    sections = {
        "📄 Overview": "",
        "🔐 Data Usage": "",
        "💳 Payments & Refunds": "",
        "📍 Tracking & Cookies": "",
        "⚖️ Liability & Disputes": ""
    }

    sentences = raw_summary.split(". ")
    chunk_size = max(1, len(sentences) // len(sections))
    section_list = list(sections.keys())

    idx = 0
    for i, sentence in enumerate(sentences):
        sections[section_list[idx]] += sentence.strip() + ". "
        if (i + 1) % chunk_size == 0 and idx < len(section_list) - 1:
            idx += 1

    # Combine into final structured summary
    final_summary = "\n\n".join([f"{title}:\n{content.strip()}" for title, content in sections.items()])
    return final_summary

def tag_risks(summary: str):
    """
    Scan the summary for risk keywords and return tags list.
    """
    found_tags = []
    lower_summary = summary.lower()
    for tag, phrases in RISK_KEYWORDS.items():
        for phrase in phrases:
            if phrase in lower_summary:
                found_tags.append(tag)
                break
    return list(set(found_tags))
