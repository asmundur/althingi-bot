
import BIN_manipulator
import datetime
import markovify
# corpus = open('althingi2.txt')
# gen = Markov(corpus)


def generate_correct_text(seed, max_length):
    return_str = ''
    parts = seed.split()

    i = 0
    try:
        if len(parts) == 1:
            while True:
                return_str = gen.generate_markov_text(seed=seed, max_size=max_length)
                if BIN_manipulator.is_grammatically_correct(return_str):
                    return return_str

        while True :

            return_str = gen.generate_markov_text(seed = [parts[i],parts[i+1]], max_size=max_length)
            if BIN_manipulator.is_grammatically_correct(return_str) :
                return return_str
            i += 1
            if i+1 >= len(parts) :
                i = 0

    except Exception as e:
        print(datetime.datetime.now())
        print('Markov model fail')
        print(str(e))
        return 'FAIL'

def get_corpus():
    """
    Reads all files in the data directory and returns a Markovify model
    that can be used to build sentences
    """
    all_text = []

    with open('althing2_cleaned.txt', 'r') as article:
        # Quotation marks rarely come out as pairs in finished chains.
        # So we remove them before adding the article text:
        all_text.append(article.read())

    return markovify.Text(all_text, state_size=5, retain_original=False)

def create_tweet(fromText):
    """
    Returns a short sentence (maximum 140 characters) from a given model
    """
    return model.make_sentence_with_start(fromText, max_words = 20)
print(datetime.datetime.now())
model = get_corpus()
#print(create_tweet(model))
print(datetime.datetime.now())

