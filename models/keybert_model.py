from keybert import KeyBERT
import sys

kw_model = KeyBERT()

if __name__ == "__main__":
  text = sys.argv[1]
  keywords = kw_model.extract_keywords(text)
  print(keywords)