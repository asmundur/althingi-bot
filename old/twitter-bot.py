consumer_key = '0N7Nhj53AudrQBmEXcJYjNkhp'
consumer_secret = 'y0FlTCIgqccdmlcHEDAK1Mk4EqeJyFJ9lIJaS6yIclbEeaRVZ8'
access_token_key = '1110625503596236801-LiZUMms0vMyIP0NqYCWdAsfr2Jg1I6'
access_token_secret = '27b9xem8qIb0qUK7MShBfGFkCAwzA2ztyNuMCnUAbfCU3'

import twitter
from textgenrnn import textgenrnn
import time
import random
import datetime

textgen = textgenrnn(weights_path='model/colaboratory_weights.hdf5',
                       vocab_path='model/colaboratory_vocab.json',
                       config_path='model/colaboratory_config.json')


while True :
    try:
        api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
        str_list = textgen.generate(max_gen_length=180, return_as_list=True, temperature=0.65)
        status = api.PostUpdate(str(str_list[0]))
        print(status.text)
        
    except Exception as e:
        print(datetime.datetime.now())
        print('Failed to post tweet')
        print(str(e))
    print('sleep at:')
    print(datetime.datetime.now())
    minuteWait = 60*random.randint(2,5)
    print('for {} minutes'.format(minuteWait))
    time.sleep(60 * minuteWait ) #set to 15 minutes for now to populate tweets. Will increase later
