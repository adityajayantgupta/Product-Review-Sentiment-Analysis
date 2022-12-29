from happytransformer import HappyTextClassification

happy_tc = HappyTextClassification(model_type="DISTILBERT", model_name="distilbert-base-uncased-finetuned-sst-2-english", num_labels=2)

def get_sentiments(text):
    return happy_tc.classify_text(text)