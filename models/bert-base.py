from happytransformer import HappyTextClassification
import sys

happy_tc = HappyTextClassification(model_type="BERT", model_name="nlptown/bert-base-multilingual-uncased-sentiment",num_labels=5)

if __name__ == "__main__":
    text = sys.argv[1]
    print(happy_tc.classify_text(text))