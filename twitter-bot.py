
#import twitter
from TwitterAPI import TwitterAPI
from textgenrnn import textgenrnn
import time
from markovgen import Markov
from reynir import Reynir
import random 
import datetime
import sys
import threading
import BIN_manipulator
import markov_generator
import re
class TweetListener (threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self)
    def run (self):
        user_id = '1110625503596236801'
        api = getApi()
        r = api.request('statuses/filter', {'follow': user_id})
        for item in r:
            print(str(item))
            sender_tweet_id = item['id'] if 'id' in item else ''
            sender_user_id = item['user']['id_str'] if 'id_str' in item else ''
            sender_user_name = item['user']['screen_name'] if 'user' in item and 'screen_name' in item['user'] else ''
            sender_tweet_text = item['text'] if 'text' in item else ''

            if sender_tweet_text != '' and sender_tweet_id != '' and sender_user_id != '' and sender_user_name != '' and user_id != sender_user_id:
                answer_to_tweet(sender_tweet_text, sender_tweet_id, sender_user_name)



def getApi() : 
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
        
    return api

def answer_to_tweet(tweet_text, tweet_id, username):
    api = getApi()

    cleaned_tweet_text = remove_username_handle_and_clean(tweet_text)
    print('cleaned_tweet_text')
    print(cleaned_tweet_text)
    seed = BIN_manipulator.manipulate_string(cleaned_tweet_text)
    print('seed')
    print(seed)
    text = markov_generator.generate_correct_text(seed, 20)
    print('text')
    print(text)
    if text == 'FAIL':
        str_list = textgen.generate(max_gen_length=180, return_as_list=True, temperature=0.65, prefix=seed)
        text = str_list[0]
        print(text)
    response = f'@{username} {text}'
    status = api.request('statuses/update', {'status': response, 'in_reply_to_status_id': tweet_id })
    print(status.status_code)

def remove_username_handle_and_clean(tweet):
    words = tweet.split()
    length_of_handle = len(words[0])
    cleaner_text = tweet[length_of_handle+1:]
    no_handles_text =  re.sub('@', '', cleaner_text)
    print (no_handles_text)
    no_hashtags_text = re.sub('\#[^\s]*','',no_handles_text)
    return no_hashtags_text



textgen = textgenrnn(weights_path='model/colaboratory_weights.hdf5',
        vocab_path='model/colaboratory_vocab.json',
        config_path='model/colaboratory_config.json')
# corpus = open('althingi2.txt')
#gen = Markov(corpus)
r = Reynir()
debug = len(sys.argv) > 1

api = getApi()

# def is_non_type(tree):
#     return type(referenceSent.tree) == type(tree)
# def get_noun_phrase(tree) :
#     if is_non_type(tree) :
#         return 'NO'
#     if(tree.is_terminal):
#         return 'NO'
#     if 'NP' == tree.tag:
#         print(tree.fl)
#         return tree.text
#     for child in tree.children:
#         string = explore_tree(child)
#         if string != 'NO':
#             return string
#     return 'NO'



TweetListener().start()
referenceSent = r.parse_single('Í fréttum er þetta helst') # Parsing a sentance that I know is correct, to use to see if parse tree is correct 
while True :
    try:
        rand = 1 # random.randint(0,1)
        # if rand == 0:
        #     print('Markov')
        #     while True :
        #         firstWord = gen.generate_markov_text(0)
        #         #sent = r.parse_single(firstWord)
        #         #print(sent)
        #         #while type(referenceSent.tree) != type(sent.tree)  or len(sent.tree.nouns) == 0 :
        #         #while True :
        #         #    firstWord = gen.generate_markov_text(0)
        #         #    sent = r.parse_single(firstWord)
        #         #    if type(referenceSent.tree) == type(sent.tree) :
        #         #        if len(sent.tree.nouns) == 0 :
        #         #            break
        #         message = gen.generate_markov_text(10)
        #         sent = r.parse_single(message)
        #         if type(referenceSent.tree) == type(sent.tree) :
        #             break
        #
        #     str_list = [message.capitalize()]
        #
        # else :
        print("Neural network")
        while True :
            str_list = textgen.generate(max_gen_length=180, return_as_list=True, temperature=0.65)
            # sent = r.parse_single(str_list[0])
            # print(str(str_list[0]))
            # if type(referenceSent.tree) == type(sent.tree) :
            #     break
            if BIN_manipulator.is_grammatically_correct(str_list[0]):
                break
        print('Final text: ' + str(str_list[0]))
        if not debug : 

            api = getApi()
            status = api.request('statuses/update', {'status' :  str(str_list[0])})
            print(status.status_code)
        else : 
            print("DEBUG MODE")
            print(str_list[0])
            print("END")
        
    except Exception as e:
        print(datetime.datetime.now())
        print('Failed to post tweet')
        print(str(e))    

    rand = random.randint(1,7)
    print('sleep at:')
    print(datetime.datetime.now())
    
    print("going to sleep for {} hours.".format(rand))
    if debug :
        factor = 60
    else : 
        factor = 60 * 60
    time.sleep(factor * rand)
