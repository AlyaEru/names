from django.shortcuts import render, redirect
from django.http import JsonResponse
from spew.models import Word, NameGroup
import random
import re

tags_list = [
    ('[NAME]','[na]'),
    ('[NOUN]','[no]'),
    ('[PNOUN]','[pn]'),
    ('[ADJ]','[ad]'),
    ('[ADV]','[av]'),
    ('[SEN]','[se]'),
    ('[SEN?]','[s?]'),
    ('[REP]','[re]')
]

def get_random_item(pos, group):
    words = Word.objects.filter(partOfSpeech__exact=pos, group__exact=group)
    if len(words) > 0:
        return str(random.choice(words))
    else: return 'NONE ):'

def a_to_an(sen):
    new = sen
    for vowel in ['a', 'e', 'i', 'o', 'u']:
        new = re.sub(r' a ' + vowel, ' an ' + vowel, new)
        new = re.sub(r'^a ' + vowel, 'an ' + vowel, new)
    return new

def pluralize(word):
    if word[-1] in ['s','x','h','z']:
        return word + 'es'
    elif len(word) > 1 and word[-1] == 'y' and word[-2] not in ['a','e','o']:
        return word[:-1] + 'ies'
    elif len(word) > 1 and word[-2:] == 'us':
        return word[:-2] + 'i'
    else: return word + 's'
    

def user_to_backend_tags(w):
    new = w
    for tag in tags_list:
        replacer = re.compile(re.escape(tag[0]), re.IGNORECASE)
        new = replacer.sub(tag[1], new)
    return new

def backend_to_user_tags(w):
    new = w
    for tag in tags_list:
        new = new.replace(tag[1], tag[0])
    return new

def cap_and_punc(sentence):
    return sentence[0].upper() + sentence[1:] + ('.' if sentence[-1] != '?' else '')

def get_sentence(request):
    groupName = request.session['group']
    group = NameGroup.objects.filter(name__exact=groupName)[:1].get()
    
    words = Word.objects.filter(partOfSpeech__exact='se', group__exact=group) | Word.objects.filter(partOfSpeech__exact='s?', group__exact=group)
    if len(words) > 0:
        sentence = str(random.choice(words))
    else: sentence = "No sentences yet; add one!"
    

    iterations = 7
    while '[' in sentence and iterations > 0:
        tags = re.findall('\[..\]',sentence)
        last = ""
        for tag in tags:
            if tag == '[re]':
                newItem = last
            elif tag == '[pn]':
                newItem = pluralize(get_random_item('no',group))
            else: newItem = get_random_item(tag[1:-1],group) 
            sentence = sentence.replace(tag, newItem,1)
            #BUG: if already replaced tag has same part of speech, will
            #   replace that tag (doing next round early). could mess up
            #   rep tag or future things. FIX: build newSentence, blank out tags
            #   in sentence when they've been filled in newSentence?

            last = newItem
            iterations -= 1
    sentence = a_to_an(sentence)
    sentence = cap_and_punc(sentence)
    data = { 'sentence': sentence }
    return JsonResponse(data)

def new_word(request):
    word = request.GET.get('word', None)
    pos = request.GET.get('pos', None)
    groupName = request.session['group']
    group = NameGroup.objects.filter(name__exact=groupName)[:1].get()
    
    if word and pos:
        if Word.objects.filter(partOfSpeech__exact=pos, word__exact=word, group__name__exact=groupName).count() == 0:
            if word[-1] == '?' and pos == 'se':
                pos = 's?'
            dbword = user_to_backend_tags(word)
            w = Word(word=dbword, partOfSpeech=pos, group=group)
            w.save()
        else:
            return JsonResponse({ 'response': backend_to_user_tags(word) + ' already exists'})

    return JsonResponse({ 'response': word + ' added to database'})

def delete_word(request):
    word = request.GET.get('word', None)
    pos = request.GET.get('pos', None)
    groupName = request.session['group']

    group = NameGroup.objects.filter(name__exact=groupName)[:1].get()
    dbword = user_to_backend_tags(word)
    Word.objects.filter(partOfSpeech__exact=pos, word__exact=dbword, group__exact=group).delete()

    return JsonResponse({ 'response': word + ' deleted from database'})


def index(request):
    if 'group' in request.session.keys():
        return render(request, 'index.html', {'group': request.session['group']})
    else: return redirect('./groups')

def join_group(request):
    name = request.GET.get('name', None)
    pwd = request.GET.get('pwd', None)

    group = NameGroup.objects.filter(name__exact=name)
    
    if len(group) == 1:
        group = group[0]
        #check password
        if group.password != pwd:
            #error message, password is incorrect
            return JsonResponse({'success': -1, 'message': 'wrong password'})
        #navigate to page, give group info
        request.session['group'] = name
        return JsonResponse({'success': 0, 'group': name})
    else:
        #error message, group does not exist
        return JsonResponse({'success': -1, 'message': 'group does not exist'})
    
    return JsonResponse({'success': 0, 'message': name + ' ' + pwd})

def create_group_setup(request):
    name = request.GET.get('name', None)
    pwd = request.GET.get('pwd', None)

    group = NameGroup.objects.filter(name__exact=name)
    
    if len(group) == 0:
        return JsonResponse({'success': 0, 'message': 'success'})
    else:
        #if there is one already, can't add another
        return JsonResponse({'success': -1, 'message': 'a group with this name already exists'})

def create_group(request):
    name = request.GET.get('name', None)
    pwd = request.GET.get('pwd', None)

    group = NameGroup.objects.filter(name__exact=name)

    if len(group) == 0:
        g = NameGroup(name=name, password=pwd)
        g.save()
        request.session['group'] = name
        return JsonResponse({'success': 0, 'message': 'success'})
    else:
        #if there is one already, can't add another
        return JsonResponse({'success': -1, 'message': 'a group with this name already exists'})

    

def groupselect(request):
    return render(request, 'groupselect.html')


