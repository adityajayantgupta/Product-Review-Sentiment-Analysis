from joblib import Memory
from transformers import pipeline

model_name = "LiYuan/amazon-review-sentiment-analysis"
sentiment_pipeline = pipeline("text-classification", model=model_name)

memory = Memory(location='cache_dir', verbose=0)
@memory.cache
def SentimentAnalyzer(reviews):
    print("sentiment_analyzer called")
    scores = []
    for r in reviews:
        if len(r) > 512:
            # Split the review into chunks of maximum length 512 sequences
            chunks = [r[i:i+512] for i in range(0, len(r), 512)]
            # Analyze each chunk separately and aggregate the results
            chunk_scores = [sentiment_pipeline(c)[0]['label'].split(" ")[0] for c in chunks]
            score = sum(float(s) for s in chunk_scores) / len(chunk_scores)
        else:
            result = sentiment_pipeline(r)
            label = result[0]['label']
            score = label.split(" ")[0]
        scores.append(float(score))
    if len(scores) > 0:
        return sum(scores) / len(scores)
    else:
        return 0.0
