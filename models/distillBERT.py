from happytransformer import HappyTextClassification
import sys


happy_tc = HappyTextClassification(model_type="DISTILBERT", model_name="distilbert-base-uncased-finetuned-sst-2-english", num_labels=2)

if __name__ == "__main__":
    text = sys.argv[1]
    print(happy_tc.classify_text(text))