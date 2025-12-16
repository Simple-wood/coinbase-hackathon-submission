from transformers import pipeline 

classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

def match(data, labels):
    response = classifier(data, labels)

    return response["labels"][0]
