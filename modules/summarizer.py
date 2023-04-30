import concurrent.futures
from joblib import Memory
from transformers import pipeline
from langdetect import detect

# Load pre-trained model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
summarizer = pipeline("summarization")

# Set up cache memory
memory = Memory(location='cache_dir', verbose=0)

@memory.cache
def ReviewSummarizer(reviews, max_length=150, min_length=100):
    print("review summarizer called")
    # Filter out non-English reviews
    english_reviews = [r for r in reviews if detect(r) == 'en']
    if not english_reviews:
        return ''
    
    # Concatenate reviews into one single text block
    concatenated_text = "\n".join(english_reviews)
    factor = len(concatenated_text)//1024
    if factor>0:
        max_length = max((max_length//factor), 100)

    # Split the concatenated text into chunks of 1024 tokens
    chunks = [concatenated_text[i:i+1024] for i in range(0, len(concatenated_text), 1024)]
    
    def summarize_chunk(chunk):
        summary = summarizer(chunk, max_length=max_length, do_sample=False)[0]['summary_text']
        return summary
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Summarize each chunk separately in parallel
        summaries = list(executor.map(summarize_chunk, chunks))

    # Join the summaries into one single text block
    summary_text = "\n".join(summaries)
    return summary_text
