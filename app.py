from scrapers.sc_amzn import get_amz_product_data, extract_reviews
from scrapers.sc_flpkrt import get_flp_product_data, extract_flp_reviews
from flask import Flask, request, render_template, jsonify
from happytransformer import HappyTextClassification
from keybert import KeyBERT
from transformers import pipeline

happy_tc = HappyTextClassification(model_type="BERT", model_name="nlptown/bert-base-multilingual-uncased-sentiment",num_labels=5)
kw_model = KeyBERT()
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
  
def count_words(text):
  text = text.split(" ")
  return len(text)

def summarize_text(text: str, max_len: int) -> str:
  try:
      summary = summarizer(text, max_length=max_len, min_length=10, do_sample=False)
      return summary[0]["summary_text"]
  except:
      print("Sequence length too large for model, cutting text in half and calling again")
      return summarize_text(text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

def get_analysis(url_amz=None, url_flp=None):
  if not url_amz and not url_flp:
    return "Nothing to analyze"

  reviews = []
  if url_amz and url_flp:
    reviews = extract_reviews(url_amz,1)
    reviews.extend(extract_flp_reviews(url_flp, 1))
  elif url_amz:
    reviews = extract_reviews(url_amz,1)
  elif url_flp:
    reviews = extract_flp_reviews(url_flp, 1)
  
  score = []
  keywords = []
  summaries = []
  for r in reviews:
    score.append(happy_tc.classify_text(r).label)
    keywords.append(kw_model.extract_keywords(r,keyphrase_ngram_range=(1,3))[0][0])
  summaries.append(summarize_text(''.join(reviews),200))

  return {"keywords":keywords, "scores": score, "summaries": summaries}

def get_product_data(url_amz=None, url_flp=None):
  productData = {}
  if url_amz and url_flp:
    productData["amazon"] = get_amz_product_data(url_amz)
    productData["flipkart"] = get_flp_product_data(url_flp)
  elif url_amz:
    productData["amazon"] = get_amz_product_data(url_amz)
  return productData

app = Flask(__name__, template_folder="templates/build", static_folder="templates/build/static")

@app.route('/')
def home():
  return render_template('index.html')


@app.route('/analyze', methods=['GET'])
def analyze():
    args = request.args
    result = {"productData": '', "analysis": ''}
    if args.get("url_amz") and args.get("url_flp"):
      result["analysis"] = get_analysis(args.get("url_amz"), args.get("url_flp"))
      result["productData"] = get_product_data(args.get("url_amz"), args.get("url_flp"))
    elif args.get("url_amz"):
      result["analysis"] = get_analysis(args.get("url_amz"), None)      
      result["productData"] = get_product_data(args.get("url_amz"), None)
    elif args.get("url_flp"):
      result["analysis"] = get_analysis(None, args.get("url_flp"))      
      result["productData"] = get_product_data(None, args.get("url_flp"))
    return jsonify(result)