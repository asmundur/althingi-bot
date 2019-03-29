import os
from lxml import etree



# file = open("althingi.txt", "a")
# file = open("test.txt", "a")
# file.writelines()
# file.writelines(['flerp','derp'])
# file.close()
def parseFile(fileName):
    tree = etree.parse(fullname)
    # for el in tree.findall('text'):
    #     print('-------------------')
    #     for ch in el.getchildren():
    #         print(ch)
    eEreeRoot = tree.getroot()
    #print(etree.tostring(eEreeRoot, pretty_print=True, encoding=str))
    child1 = eEreeRoot[1]
    subtags = list(child1)
    body = subtags[0]
    subtags = list(body)
    div = body[0]
    paragraphs = list(div)
    sentences = []
    for paragraph in paragraphs:
        newSentences =  parseParagraph(paragraph)
        sentences.extend(newSentences)
    file = open("althingi4.txt", "a")
    file.write('\n'.join(sentences) + '\n')
    file.close()

def parseParagraph(paragraph):
    sentences = []
    for sentence in list(paragraph):
        sentenceString = parseSentence(sentence)
        sentences.append(sentenceString)
    return sentences

def parseSentence(sentence):
    words = []
    for word in list(sentence):
        words.append(word.text)

    return " ".join(words)

path = "/home/alma/maltaekni/althingi_2013plus/2017"
x = os.walk(path)
for root, dirs, files in x:
    #print(root, "consumes", end=" ")
    #print(sum(os.path.getsize(os.path.join(root, name)) for name in files), end=" ")
    #print("bytes in", len(files), "non-directory files")
    for filename in files:
        if not filename.endswith('xml'): continue
        fullname = os.path.join(root, filename)
        parseFile(fullname)
        #print(list(root2))
#
#
#     # for filename in os.listdir(path):
#     #     if not filename.endswith('xml'): continue
#     #     fullname = os.path.join(path, filename)
#     #     tree = ET.parse(fullname)
#     #     root = tree.getroot()
#     #     # print(etree.tostring(root, pretty_print=True))



# file.close()
print("DONE!!!!")