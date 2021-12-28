import requests
from bs4 import BeautifulSoup
import re
import nltk
import nltk.data
from html import unescape

def remove_tags(test_str):
    ret = ''
    skip1c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif skip1c == 0:
            ret += i
    return ret

def generate_sentences(lang):
    sentences = []

    wiki_pre = 'de'
    if lang == 'german':
        wiki_pre = 'de'
    elif lang == 'czech':
        wiki_pre = 'cs'

    while len(sentences) < 10:
        response = requests.request("GET","https://{}.wikipedia.org/api/rest_v1/page/random/html".format(wiki_pre))
        soup = BeautifulSoup(response.text, features="html.parser")
        l = soup.find_all('p')
        for i in range(len(l)):
            for sent in nltk.sent_tokenize(l[i].text,language=lang):
                sent = unescape(sent)
                sent = remove_tags(sent)
                if len(sent) >= 20 and len(sent) <= 100 and sent[0].isupper() and sent[-1]=='.':
                    usable = True
                    for char in sent:
                        if not (char.isalpha() or char.isnumeric() or char in [' ','.',',','(',')','-','!','?','–',':']):
                            usable = False
                    if usable:
                        sentences.append(sent)
                    if len(sentences) >= 10:
                        return sentences
    
if __name__ == '__main__':
    print(generate_sentences('czech'))