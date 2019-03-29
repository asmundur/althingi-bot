import twitter
from textgenrnn import textgenrnn
import time

textgen = textgenrnn(weights_path='model/colaboratory_weights.hdf5',
                       vocab_path='model/colaboratory_vocab.json',
                       config_path='model/colaboratory_config.json')


while True :
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
    str_list = textgen.generate(max_gen_length=180, return_as_list=True, temperature=0.8)
    status = api.PostUpdate(str(str_list[0]))
    print(status.text)
    time.sleep(60 * 15) #set to 15 minutes for now to populate tweets. Will increase later
