import BIN_manipulator
import re
import sed
import os
import sys
import markov_generator

def main():
    while True:
        text = input('Enter your input\n')
        if text == "exit":
            break
        #new_str = BIN_manipulator.manipulate_string(text)
        # new_str = remove_username_handle_and_clean(text)
        new_str = markov_generator.create_tweet(text)
        print(new_str)

main()
def clean_corpus():

    sed.sed(' \.', '.', sys.argv[1], dest='temp1.txt')
    sed.sed(' ,', ',', 'temp1.txt', dest='temp2.txt')
    sed.sed(' :', ':', 'temp2.txt', dest='temp3.txt')
    sed.sed(' ;', ';', 'temp3.txt', dest='temp4.txt')
    sed.sed(' ;', ';', 'temp3.txt', dest='temp4.txt')
    sed.sed(' !', '!', 'temp4.txt', dest='temp6.txt')
    #sed.sed('\n', ' ', 'temp5.txt', dest='temp6.txt')
    sed.sed('\(.*\)', '', 'temp6.txt', dest='temp7.txt')
    sed.sed(' +', ' ', 'temp7.txt', dest='temp8.txt')
    sed.sed(' \?', '?', 'temp8.txt', dest=sys.argv[2])
    number = 1
    while number < 9 :
        os.system('rm temp{0}.txt'.format(number))
        number += 1
#clean_corpus()

