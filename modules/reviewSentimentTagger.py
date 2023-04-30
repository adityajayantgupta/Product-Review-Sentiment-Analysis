from joblib import Memory
from transformers import pipeline

model_name = "LiYuan/amazon-review-sentiment-analysis"
sentiment_pipeline = pipeline("text-classification", model=model_name)

memory = Memory(location='cache_dir', verbose=0)

@memory.cache
def ReviewSentimentTagger(review):
    print("sentiment_analyzer called")
    sentences = review.split('.')
    tagged_sentences = []
    for sentence in sentences:
        result = sentiment_pipeline(sentence)
        label = result[0]['label']
        score = int(label.split(" ")[0])
        color = ""
        if score == 5:
            color = "green"
        elif score == 4:
            color = "lightgreen"
        elif score == 3:
            color = "yellow"
        elif score == 2:
            color = "orange"
        else:
            color = "red"
        tagged_sentence = f"<span data-highlight={color}>{sentence}</span>"
        tagged_sentences.append(tagged_sentence)
    return " ".join(tagged_sentences)