from keybert import KeyBERT

kw_model = KeyBERT()

def get_keywords(text):
  keywords = kw_model.extract_keywords(text,keyphrase_ngram_range=(1,3))
  return keywords