import fasttext
hyper_params = {
    "lr": 0.01,
    "epoch": 15,
    "wordNgrams": 2,
    "dim": 20,
    "verbose": 1
}

model = fasttext.load_model("model_amzn.bin")

result = model.predict("model_amzn.bin", "i love this product")

print("Result: ", result)
