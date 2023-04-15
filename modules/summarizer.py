from joblib import Memory
from transformers import pipeline

# Load pre-trained model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
summarizer = pipeline("summarization", model=model_name, tokenizer=model_name)

# Set up cache memory
memory = Memory(location='cache_dir', verbose=0)

@memory.cache
def ReviewSummarizer(reviews, max_length=150, min_length=100):
  # Concatenate reviews into one single text block
  print("review summarizer called")
  concatenated_text = "\n".join(reviews)
  # Split the concatenated text into chunks of 1024 tokens
  chunks = [concatenated_text[i:i+1024] for i in range(0, len(concatenated_text), 1024)]
  # Summarize each chunk separately
  summaries = []
  for chunk in chunks:
    summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    summaries.append(summary)
  # Join the summaries into one single text block
  summary_text = "\n".join(summaries)
  return summary_text