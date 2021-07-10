from nltk import classify
from nltk import FreqDist
from nltk import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import pickle
import random
import re
import string

class NltkManager:
    def lemmatize_sentence(self, tokens):
        lemmatizer = WordNetLemmatizer()
        lemmatized_sentence = []
        for word, tag in pos_tag(tokens):
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
        return lemmatized_sentence

    def remove_noise(self, tweet_tokens, stop_words = ()):

        cleaned_tokens = []

        for token, tag in pos_tag(tweet_tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                           '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens

    def get_all_words(self, cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            for token in tokens:
                yield token

    def get_tweets_for_model(self, cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)

    def save_model(self, classifier):
        f = open('nltk/model/my_classifier.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()

    def load_model(self, path = 'nltk/model/my_classifier.pickle'):
        f = open(path, 'rb')
        classifier = pickle.load(f)
        f.close()
        return classifier

    def train_data(self):
        positive_tweets = twitter_samples.strings('positive_tweets.json')
        negative_tweets = twitter_samples.strings('negative_tweets.json')
        text = twitter_samples.strings('tweets.20150430-223406.json')

        stop_words = stopwords.words('english')

        positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
        negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

        positive_cleaned_tokens_list = []
        negative_cleaned_tokens_list = []

        for tokens in positive_tweet_tokens:
            positive_cleaned_tokens_list.append(self.remove_noise(tokens, stop_words))

        for tokens in negative_tweet_tokens:
            negative_cleaned_tokens_list.append(self.remove_noise(tokens, stop_words))

        # all_pos_words = self.get_all_words(positive_cleaned_tokens_list)

        positive_tokens_for_model = self.get_tweets_for_model(positive_cleaned_tokens_list)
        negative_tokens_for_model = self.get_tweets_for_model(negative_cleaned_tokens_list)

        positive_dataset = [(tweet_dict, "Positive")
                             for tweet_dict in positive_tokens_for_model]

        negative_dataset = [(tweet_dict, "Negative")
                             for tweet_dict in negative_tokens_for_model]

        dataset = positive_dataset + negative_dataset

        random.shuffle(dataset)

        train_data = dataset[:7000]
        test_data = dataset[7000:]

        classifier = NaiveBayesClassifier.train(train_data)

        self.save_model(classifier)

        print("Accuracy is:", classify.accuracy(classifier, test_data))

        print(classifier.show_most_informative_features(10))

    def predict(self, classifier, text):
        custom_tokens = self.remove_noise(word_tokenize(text))

        print(classifier.classify(dict([token, True] for token in custom_tokens)))