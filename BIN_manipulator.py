from reynir import Reynir
import sys
from markovgen import Markov
import time
import datetime
import re

#corpus = open('althingi2.txt')
#gen = Markov(corpus)


r = Reynir()
referenceSent = r.parse_single('Í fréttum er þetta helst')

def is_grammatically_correct(test_string):
    sent = r.parse_single(test_string)
    return not is_non_type(sent.tree)

def is_non_type(tree):
    return type(referenceSent.tree) != type(tree)

def count_unique_words_in_BIN_list(lis):
    ids = []
    for item in lis :
        ids.append(item[1])

    return len(set(ids))

def BIN_field_count():
    count_list = []
    with open('SHsnid/SHsnid_extra.csv') as handle :
        for line in handle :
            parts = line.split(sep=';')
            if len(parts) not in count_list:
                print(parts)
                count_list.append(len(parts))

    print(count_list)



def number_unambiguity_in_BIN_list(lis):
    singular_count = 0
    for item in lis :
        if 'ET' in item[5]:
            singular_count += 1
    return singular_count == 0 or singular_count == len(lis)

def find_all_in_BIN(word, group, lemma, number = '', gender = ''):
    words = []
    word = word.lower()
    gender = gender.upper()

    with open('SHsnid/SHsnid_extra.csv', 'r') as handle:
        no_of_words = 0
        for line in handle:

            parts = line.split(sep=';')
            if word == (parts[4]).lower() and group == parts[2] and lemma == parts[0] and number in parts[5] and gender in parts[5]:
                no_of_words += 1
                words.append(parts)
                #print(parts)
            #print(parts)
            #time.sleep(1)
        print('==')
        print(word)
        print("{} exact matches found in BIN".format(no_of_words))
        print("{} unique words found in BIN".format(count_unique_words_in_BIN_list(words)))
        print('==')
    return words

def get_noun_case_string(BIN_item, desired_case, number):
    caseString = '{0}{1}gr\n'.format(desired_case, number)
    caseStringFallback = '{0}{1}\n'.format(desired_case, number) # if noun doesn't take an article

    return (caseString,caseStringFallback)

def get_adj_case_string(BIN_item, desired_case, has_article) :
    old_case_str = BIN_item[5]
    number = ''
    if 'ET' in old_case_str :
        number = 'ET'
    else :
        number = 'FT'
    gender = ''
    if 'HK' in old_case_str :
        gender = 'HK'
    elif 'KVK' in old_case_str :
        gender = 'KVK'
    else :
        gender = 'KK'
    form = old_case_str[0]
    infl_str = '' #don't really know what to name veik/sterk beyging in english
    if has_article and form != 'M' :
        infl_str = 'VB'
    elif form == 'M' :
        infl_str = 'ST'
    else :
        infl_str = 'SB'

    return '{0}{1}-{2}-{3}{4}\n'.format(form, infl_str, gender, desired_case, number)

def get_pronoun_case_str(BIN_item, desired_case) :
    gender = BIN_item[5].split(sep='-')[0]
    case_str = '{0}-{1}{2}'.format(gender, desired_case, BIN_item[5][-3:])
    return case_str

def get_personal_pronoun_case_str(BIN_item, desired_case) :
    case_str = '{0}{1}'.format(desired_case, BIN_item[5][-3:])
    return case_str

def get_number_case_str(BIN_item, desired_case) :
    gender = BIN_item[5].split(sep='_')[0]
    endlength = -3
    if BIN_item[5][-2:] == '2\n':
        endlength = -4
    case_str = '{0}_{1}{2}'.format(gender, desired_case, BIN_item[5][endlength:])
    return case_str

def get_article_case_str(BIN_item, desired_case):
    gender = BIN_item[5].split(sep='_')[0]
    case_str = '{0}_{1}{2}'.format(gender, desired_case, BIN_item[5][-3:])
    return case_str

def get_word_in_case(word_id, case_string):
    if case_string[-1:] != '\n':
        case_string = case_string + '\n'

    with open('SHsnid/SHsnid_extra.csv', 'r') as handle:
        for line in handle :
            parts = line.split(sep=';')
            if parts[1] == word_id and case_string == parts[5]:
                return parts[4]

    return 'NOT FOUND'


def fix_noun_with_BIN(word, desired_case, gender, lemma, no_article, number) :

    final_word = '{}'
    word_with_article_not_found = False
    words = find_all_in_BIN(word, gender, lemma, number)
    print(words)
    if count_unique_words_in_BIN_list(words) == 1 : #handle it if this isn't the case
        if number_unambiguity_in_BIN_list(words):
            (case_string,case_string_fallback) = get_noun_case_string(words[0], desired_case, number)
            #print(case_string)
            word = get_word_in_case(words[0][1], case_string)

            if word == 'NOT FOUND' or no_article :
                word = get_word_in_case(words[0][1], case_string_fallback)

            return word
        else : # TODO
            print("Number ambiguious")

            return "NOT FOUND"
    elif count_unique_words_in_BIN_list(words) == 0 :
        print("0 matches found in BIN")
        print(datetime.datetime.now())
        return "NOT FOUND"

    else : #TODO handle this
        print('Words ambiguious')
        print(wrds)

        return 'NOT FOUND'

#while True :
#    print(fix_noun_with_BIN(input('Enter your input: ').lower()))

def find_first_NP_in_tree(tree) :
    if is_non_type(tree) :
        return 'NO'
    if(tree.is_terminal):
        return 'NO'
    if 'NP' in tree.tag:
        #print(tree.fl)
        return tree.text
    for child in tree.children:
        string = find_first_NP_in_tree(child)
        if string != 'NO':
            return string
    return 'NO'

# code snippet got from stackoverflow
# https://stackoverflow.com/questions/17870544/find-starting-and-ending-indices-of-sublist-in-list
def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll-1))

    return results

def get_node_list_for_NP_string(NP_string, node_list) :
    initial_index = 0
    parts = NP_string.split()
    word_list = []
    for node in node_list :
        word_list.append(node['x'])
    indices = find_sub_list(parts, word_list)

    return node_list[indices[0][0]:indices[0][1]+1]

def convert_trees_to_dicts(tree_list):
    ret_list = []
    for tree in tree_list:
        proto_dict = tree.__dict__
        ret_list.append(proto_dict["_head"])
    return ret_list


def is_a_declension_word(word_group):
    return word_group in ['hk','kk','kvk','lo','pfn','fn','to','gr']

def swapPositions(lis, pos1, pos2) :
    lis[pos1], lis[pos2] = lis[pos2], lis[pos1]
    return lis

def handle_nouns(node, explicit_article) :
    number = ''
    if 'b' not in node:
        number = 'ET'
    elif 'ET' in node['b']:
        number = 'ET'
    else:
        number = 'FT'
    old_word = node['x']

    word = fix_noun_with_BIN(node['x'], desired_case='NF', gender=node['c'], lemma=node['s'],
                             no_article=explicit_article, number=number)
    if word == 'NOT FOUND':
        return word
    elif old_word[0].isupper():
        word = word.capitalize()
    return word

def handle_adjectives(node):
    word_group = node['c']
    gender = node['b'].split(sep='-')[1]
    BIN_items = find_all_in_BIN(node['x'], word_group, node['s'], node['b'][-2:], gender=gender)
    if len(BIN_items) == 0:
        return 'NOT FOUND'
    elif len(BIN_items) != 1:
        print('none, or, more than one adjs found, FIX')
        print(BIN_items)
    case_str = get_adj_case_string(BIN_items[0], 'NF', True)
    print(case_str)
    word = get_word_in_case(BIN_items[0][1], case_str)
    return word



def handle_personal_pronouns(noun):
    word_group = node['c']
    case = 'NF'
    if previous_word_noun:
        case = node['b'][:-2]
    BIN_items = find_all_in_BIN(node['x'], word_group, node['s'], node['b'][-2:])
    case_str = get_personal_pronoun_case_str(BIN_items[0], case)
    if len(BIN_items) != 1:
        print('Handle this')
        print(BIN_items)
    item = BIN_items[0]
    identity = item[1]
    if identity == '999001':  # ég changed to þú
        identity = '999007'
    elif identity == '999007':  # þú changed to ég
        identity = '999001'
    elif identity == '999004':  # vér changed to þér
        identity = '999006'
    elif identity == '999006':  # þér changed to vér
        case_str = '{0}FT\n'.format(case)
        identity = '999004'
    print(case_str)
    new_word = get_word_in_case(identity, case_str)
    return new_word
    # case_str = get_pronoun_case_str(BIN_items[0], 'NF')

    # print(node)


def handle_pronouns(node) :
    word_group = node['c']
    BIN_items = find_all_in_BIN(node['x'], word_group, node['s'], node['b'][-2:])
    if len(BIN_items) != 1:
        print('Handle this')
        print(BIN_items)
    case_str = get_pronoun_case_str(BIN_items[0], 'NF')
    if BIN_items[0][0] == 'sá' or BIN_items[0][0]:
        explicit_article = True
    print(case_str)
    word = get_word_in_case(BIN_items[0][1], case_str)
    # if word == 'NOT FOUND':
    #     new_words = []
    #     return  'NOT FOUND'
    return word
def handle_numbers(node):
    word_group = node['c']
    BIN_items = find_all_in_BIN(node['x'], word_group, node['s'], node['b'][-2:])
    if len(BIN_items) != 1:
        print('Handle this')
        print(BIN_items)
    case_str = get_number_case_str(BIN_items[0], 'NF')
    word = get_word_in_case(BIN_items[0][1], case_str)
    return word

def handle_article(node):
    word_group = node['c']
    BIN_items = find_all_in_BIN(node['x'], word_group, node['s'], node['b'][-2:])
    if len(BIN_items) != 1:
        print('Handle this')
        print(BIN_items)

    case_str = get_article_case_str(BIN_items[0], 'NF')
    word = get_word_in_case(BIN_items[0][1], case_str)
    return word

def manipulate_string(sentence) :
    # text = input('Enter your input\n')
    # if text == "exit" :
    #     break

    print('#########')
    sent = r.parse_single(sentence)
    if is_non_type(sent.tree) :
        print('Could not parse sentence')
        return 'ERROR'
    NP_string = find_first_NP_in_tree(sent.tree)

    print('NP_string : {}'.format(NP_string))
    node_dicts = convert_trees_to_dicts(sent.terminal_nodes)
    nodes = get_node_list_for_NP_string(NP_string, node_dicts)
    # parts = NP_string.split()
    new_words = []
    # TODO remove this before submitting
    for node in nodes :
        print('-----')
        print(node)
        print('+++++')
    explicit_article = False
    previous_word_noun = False
    number_appeared_before = False
    current_index = 0
    word = 'NOT FOUND'
    for node in nodes:
        if 'c' not in node:
            continue
        word_group = node['c']
        if word_group == 'st':
            # new_words.append(node['x'])
            word = node['x']
            explicit_article = False
            number_appeared_before = False
            new_words.append(word)
        elif word_group == 'ao' and len(new_words) == 0 :
            print("skipping {0} at the beggining of a sentance".format(node['x']))
            continue
        elif not is_a_declension_word(word_group):
            break #decided to quit here due to lack of time, and longer sentences don't look good either
        elif word_group in ['hk','kk','kvk']:
            word = handle_nouns(node, explicit_article)
            new_words.append(word)
            if number_appeared_before:
                new_words = swapPositions(new_words, current_index, current_index - 1)
            elif current_index > 0 and not explicit_article and not number_appeared_before: #stílfærsla
                i = current_index - 1
                while i >= 0 and 'c' in nodes[i] :
                    if nodes[i]['c'] == 'lo' :
                        new_words = swapPositions(new_words, i, i+1)
                        i -= 1
                    else :
                        break

        elif word_group == 'lo':
            word = handle_adjectives(node)
            if word == 'NOT FOUND':
                new_words = []
                break
            new_words.append(word)
            if number_appeared_before:
                new_words = swapPositions(new_words, current_index, current_index - 1)
            # elif previous_word_noun and not explicit_article:
            #     new_words = swapPositions(new_words, current_index, current_index - 1)
        elif word_group == 'pfn':
            word = handle_personal_pronouns(node)
            new_words.append(word)
        elif word_group == 'fn' :
            word = handle_pronouns(node)
            new_words.append(word)
        elif word_group == 'to' :
            word = handle_numbers(node)
            previous_word_noun = False
            number_appeared_before = True
            new_words.append(word)
        else :
            explicit_article = True
            word = handle_article(node)
            new_words.append(word)

        if word_group in ['hk','kk','kvk'] :
            previous_word_noun = True
        else :
            previous_word_noun = False
        current_index += 1
        if word == 'NOT FOUND':
            new_words = []
            break

    if len(new_words) == 0:
        return 'ERROR'
    new_words[0] = new_words[0].capitalize()
    adjusted_string = ' '.join(new_words)
    return adjusted_string
        #first_word = fix_noun_with_BIN((parts[0]).lower())
        #adjusted_string = '{0} {1}'.format(first_word, NP_string[len(parts[0])+1:])
        #print(adjusted_string.capitalize())

