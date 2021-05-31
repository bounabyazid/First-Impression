import re

import pickle
import numpy, scipy.io

import inflect
from urlextract import URLExtract

from Replacers import RegexpReplacer

def WritePickle(file,Data):
    with open(file+'.pkl', 'wb') as handle:
        pickle.dump(Data, handle, protocol=pickle.HIGHEST_PROTOCOL)
#____________________________________________________________________

def ReadPickle(file):
    with open(file+'.pkl', 'rb') as handle:
        Data = pickle.load(handle)
    return Data
#____________________________________________________________________

def Extract_Numbers(string, ints=True):            
    numexp = re.compile(r'\d[\d,]*[\.]?[\d{2}]* ?')
    numbers = numexp.findall(string)
    numbers = [x.strip(' ') for x in numbers]

    return numbers
#____________________________________________________________________

def Extract_URLs(sentence):
    extractor = URLExtract()
    urls = extractor.find_urls(sentence)
    return list(set(urls))
#____________________________________________________________________

def Extract_emails(sentence):
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

    emails = re.findall(r'[\w\.-]+@[\w\.-]+', sentence)
    return list(set(emails))
#____________________________________________________________________

def List_Punctuations(text):
    text = re.sub('[A-Za-z]|[0-9]|[\n\t]|[£€$% ]','',text)
    SymbList = list(dict.fromkeys(text).keys())
    return list(set(SymbList))
#____________________________________________________________________

def Split_uppercase(value):
    S = re.sub(r'([A-Z][a-z]+)', r' \1', value)
    return re.sub(r'([A-Z]+)', r' \1', S).strip()
#____________________________________________________________________

def Extract_Acronyms(sentence):
    Acronyms = re.findall('(?:(?<=\.|\s)[A-Z]\.)+',sentence)
    return list(set(Acronyms))
#____________________________________________________________________

def PreprocessTranscript(Transcript,Urls,Emails,Punctuations,Acronyms):
    Text = re.sub('\[.*?\]', '', Transcript)
    
    RegReplacer = RegexpReplacer()
    Text = RegReplacer.replace(Text)
    
    for Url in Urls:
        if Url in Text:
           Text = Text.replace(Url,' link ')    
    for Email in Emails:
        if Email in Text:
           Text = Text.replace(Email, ' Email ')
    for Punctuation in Punctuations:
        Text = Text.replace(Punctuation,' ')
    for Acronym in Acronyms:
        Text = Text.replace(Acronym,' ')    
    
    Text = re.sub(r"\S*\d\S*", ' ', Text)
    
    #Text = Split_uppercase(Text)

    Text = re.sub(r"\s+", " ",Text)
    
    Text = Text.strip()
        
    return Text#.lower()
#____________________________________________________________________

def Preprocessing_Taranscriptions(transcriptions,Urls,Emails,Punctuations,Acronyms):
    Clean_trans = {}
    for key in transcriptions.keys():
        Clean_trans[key]= PreprocessTranscript(transcriptions[key],Urls,Emails,Punctuations,Acronyms)
    return Clean_trans
#____________________________________________________________________

def Preprocessing_Dataset():
    file = open('info/transcription_training.pkl', "rb")
    tran_train = pickle.load(file, encoding='latin1')
    Clean_trans_train = []

    file = open('info/transcription_validation.pkl', "rb")
    tran_val = pickle.load(file, encoding='latin1')
    Clean_tran_val = []
    
    file = open('info/transcription_test.pkl', "rb")
    tran_test = pickle.load(file, encoding='latin1')
    Clean_tran_test = []
    
    Text = ' '.join(tran_train.values())+' '.join(tran_val.values())+' '.join(tran_test.values())
    
    Punctuations = List_Punctuations(Text)
    Urls = Extract_URLs(Text)
    Emails = Extract_emails(Text)
    Numbers = Extract_Numbers(Text)
    Acronyms = Extract_Acronyms(Text)
    
    print(Punctuations)
    print('________________________')
    print(Urls)
    print('________________________')
    print(Emails)
    print('________________________')
    print(Numbers)
    print('________________________')
    print(Acronyms)
    
    Clean_trans_train = Preprocessing_Taranscriptions(tran_train,Urls,Emails,Punctuations,Acronyms)
    Clean_tran_val = Preprocessing_Taranscriptions(tran_val,Urls,Emails,Punctuations,Acronyms)
    Clean_tran_test = Preprocessing_Taranscriptions(tran_test,Urls,Emails,Punctuations,Acronyms)
    
    return Clean_trans_train, Clean_tran_val, Clean_tran_test, tran_train.keys(), tran_val.keys(), tran_test.keys()
