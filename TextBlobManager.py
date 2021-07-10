from textblob import TextBlob

def classify(sentence):
    test = TextBlob(sentence)
    print(test.sentiment)