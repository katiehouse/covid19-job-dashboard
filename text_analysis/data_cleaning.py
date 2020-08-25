import pandas as pd
import json
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import re
import math
import string

def read_data():
    with open('text_analysis/indeed.json') as f:
        indeed = json.load(f)
    indeed_df = pd.json_normalize(indeed)
    full_text = indeed_df['full_text']
    full_text2 = []
    for row in full_text:
        full_text2.append(row)
    full_text = ' '.join(full_text2)
    

    return(full_text)


def string_clean(full_text):
    string.punctuation = string.punctuation + "–’"
    full_text = full_text.replace('\n', ' ').lower().translate(
        str.maketrans('', '', string.punctuation))
    
    return(full_text)


def rm_stop_words(full_text):
    # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    stop_words = set(stopwords.words('english'))
    # TypeError: expected string or bytes-like object
    # right now row is a pandas series
    word_tokens = word_tokenize(full_text)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    full_text = ' '.join(filtered_sentence)
    
    return(full_text)


def data_cleaning():
    full_text = read_data()
    full_text = string_clean(full_text)
    full_text = rm_stop_words(full_text)

    return(full_text)


def remove_string_special_characters(s):
    stripped = re.sub('[^\w\s]', '', s)
    stripped = re.sub('_', '', stripped)
    stripped = re.sub('\s+', ' ', stripped)
    stripped = stripped.strip()

    return(stripped)


def get_doc(sent):
    doc_info = []
    i = 0
    for sent in text_sents_clean:
        i += 1
        count = count_words(full_text)
        temp = {'doc_id' : i, 'doc_length' : count}
        doc_info.append(temp)
    return(doc_info)

def count_words(full_text):
    count = 0
    words = word_tokenize(full_text)
    for word in words:
        count += 1
    return(count)

def create_freq_dict(sents):
    i = 0
    freqDict_list = []
    for sent in sents:
        i += 1
        freq_dict = {}
        for word in words:
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
            temp = {'doc_id' : i, 'freq_dict' : freq_dict}
        freqDict_list.append(temp)
    
    return(freqDict_list)


def computeTF(doc_info, freqDict_list):
    TF_scores = []
    for tempDict in freqDict_list:
        id = tempDict['doc_id']
        for k in tempDict['freq_dict']:
            temp = {'doc_id' : id,
                    'TF_score' : tempDict['freq_dict'][k]/doc_info[id-1]['doc_length'],
                    'key' : k}
            TF_scores.append(temp)
        
    return(TF_scores)

def computeIDF(doc_info, freqDict_list):
    IDF_scores = []
    counter = 0
    for dict in freqDict_list:
        counter += 1
        for k in dict['freq_dict'].keys():
            count = sum([k in tempDict['freq_dict'] for tempDict in freqDict_list])
            temp = {'doc_id' : counter, 'IDF_score' : math.log(len(doc_info/count)), 'key' : k}
            IDF_scores.append(temp)

    return(IDF_scores)

def computeTFIDF(TF_scores, IDF_scores):
    TFIDF_scores = []
    for j in IDF_scores:
        for i in TF_scores:
            if j['key'] -- i['key'] and j['doc_id'] == i['doc_id']:
                temp = {'doc_id' : j['doc_id'],
                        'TFIDF_score' : j['IDF_score']*i['TF_score'],
                        'key' : i['key']}
        TFIDF_scores.append(temp)
    return(TFIDF_scores)


def tf_igf(full_text):
    text_sents = sent_tokenize(full_text)
    text_sents_clean = [remove_string_special_characters(s) for s in text_sents]
    doc_info = get_doc(text_sents_clean)
    freqDict_list = create_freq_dict(text_sents_clean)
    TF_scores = computeTF(doc_info, freqDict_list)
    IDF_scores = computeIDF(doc_info, freqDict_list)
    TFIDF_scores = computeTFIDF(TF_scores, IDF_scores)
     

def main():
    data_cleaning()


if __name__ == "__main__":
    main()






    