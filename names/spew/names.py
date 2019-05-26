from spew.models import Word
import random
import re

def get_random_item(pos):
    return str(random.choice(Word.objects.filter(partOfSpeech__exact=pos)))

def get_sentence():
    sentence = get_random_item('se')
    while '[' in sentence:
        tags = re.findall('\[..\]',sentence)
        last = ""
        for tag in tags:
            newItem = last if tag == '[re]' else get_random_item(tag[1:-1]) 
            sentence = sentence.replace(tag, newItem,1)
            last = newItem
    return sentence

