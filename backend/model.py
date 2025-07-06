from transformers import pipeline, AutoTokenizer
import re

# Load tokenizer and summarizer model
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Clean input text
def clean_text(raw_text: str) -> str:
    raw_text = re.sub(r'\s+', ' ', raw_text)
    raw_text = re.sub(r'(©\s+\d{4}.*?$|Last updated.*?$)', '', raw_text, flags=re.IGNORECASE)
    return raw_text.strip()

# Chunk text by sentence and token length
def split_text(text, max_tokens=1024):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if not sentence.strip():
            continue
        prospective_chunk = current_chunk + " " + sentence if current_chunk else sentence
        token_ids = tokenizer.encode(prospective_chunk, add_special_tokens=False)
        
        # 🚫 Drop invalid chunks
        if max(token_ids) >= tokenizer.vocab_size:
            print("⚠️ Skipping chunk due to out-of-vocab token.")
            continue

        if len(token_ids) <= max_tokens:
            current_chunk = prospective_chunk
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Run summarization
def analyze_text(text: str) -> str:
    if not text.strip():
        return "No content provided."

    cleaned_text = clean_text(text)
    chunks = split_text(cleaned_text, max_tokens=1024)

    summaries = []
    for chunk in chunks:
        try:
            result = summarizer(chunk, max_length=200, min_length=40, do_sample=False)
            summaries.append(result[0]["summary_text"])
        except IndexError as e:
            print(f"❌ Skipping chunk due to error: {e}")
            continue

    return " ".join(summaries) if summaries else "⚠️ Summary could not be generated."

# Optional: tag known risk phrases
def tag_risks(summary: str) -> list:
    tags = {
        "data sharing": ["share your data", "third parties", "sell your data"],
        "no refunds": ["no refunds", "non-refundable", "cannot return"],
        "tracking": ["cookies", "track your behavior", "analytics tools"],
        "liability": ["not responsible", "no liability", "at your own risk"],
        "arbitration": ["binding arbitration", "waive your right", "no class action"]
    }

    matched_tags = []
    for tag, keywords in tags.items():
        for phrase in keywords:
            if phrase in summary.lower():
                matched_tags.append(tag)
                break

    return matched_tags
