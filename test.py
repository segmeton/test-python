import GoogleTextToSpeech
import nlp_test
import VaderManager
import TextBlobManager
import ImagePicker

def google_test(sentence):
    test = GoogleTextToSpeech.GoogleTextToSpeech()

    test.synthesize(sentence)

def nltk_test(sentence):
    manager = nlp_test.NltkManager()

    classifier = manager.load_model()

    manager.predict(classifier, sentence)

def vader_test():
    VaderManager.test_sentiment()

def vader_classify(sentence):
    VaderManager.classify_sentiment(sentence)

def textblob_classify(sentence):
    TextBlobManager.classify(sentence)
#
def pick_images():
    list =  ImagePicker.get_image_list()
    chosen = ImagePicker.sampling(list, 3)
    ImagePicker.copy_sampled_image(chosen)

def pick_images_multiple(n):
    for i in range(n):
        pick_images()

sentence = "Thank you!"
# vader_classify(sentence)
# textblob_classify(sentence)

# google_test(sentence)

pick_images_multiple(10)