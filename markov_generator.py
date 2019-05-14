from markovgen import Markov
import BIN_manipulator
import datetime
corpus = open('althingi2.txt')
gen = Markov(corpus)

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