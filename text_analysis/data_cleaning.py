import pandas as pd
import json
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

def read_data():
    with open('text_analysis/indeed.json') as f:
        indeed = json.load(f)
    indeed_df = pd.json_normalize(indeed)
    full_text = indeed_df['full_text']

    return(full_text)


def line_break(full_text):
    full_text = full_text.str.replace('\n', '\n ')
    
    return(full_text)


def to_lower(full_text):
    for row in full_text:
        row = row.lower()
    
    return(full_text)


def tokenize_row(row):
    # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(row)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    row = filtered_sentence
    
    return(row)


def rm_stop_words(full_text):
    for row in full_text:
        row = tokenize_row(row)
    return(full_text)

def data_cleaning():
    full_text = read_data()
    full_text = line_break(full_text)
    full_text = to_lower(full_text)
    full_text = rm_stop_words(full_text)
    print(full_text.head(5))


def main():
    data_cleaning()
    # clean_data()


if __name__ == "__main__":
    main()