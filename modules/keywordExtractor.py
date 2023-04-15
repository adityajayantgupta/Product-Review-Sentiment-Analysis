from keybert import KeyBERT
from joblib import Memory

kw_model = KeyBERT()

# Set up cache memory
memory = Memory(location='cache_dir', verbose=0)

@memory.cache
def KeywordExtractor(reviews):
  print("keyword extractor called")
  keywords = kw_model.extract_keywords(reviews,keyphrase_ngram_range=(1,3))
  filtered_keywords = []
  for k in keywords:
    filtered_keywords.append(k[0][0])
  return filtered_keywords