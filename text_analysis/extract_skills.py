import time
import csv
import json
from nltk import ngrams, word_tokenize
from pandas import json_normalize
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
import pandas as pd


def extract_skills(jobs):
    # read in skills corpus
    with open('text_analysis/linked_in_skills.csv') as f:
        reader = csv.reader(f)
        skills = list(reader)

    # convert skills to list of strings
    skills = [''.join(skill) for skill in skills]

    # read in .json
    # with open('text_analysis/indeed.json') as f:
    #         indeed = json.load(f)
    indeed_df = json_normalize(jobs)

    # select only necessary column
    full_text = indeed_df['full_text']

    # combine into 1 string
    full_text2 = []
    for row in full_text:
        full_text2.append(row)
    full_text = ' '.join(full_text2)

    # data cleaning
    full_text = full_text.replace('\n', ' ').lower()
    full_text = full_text.replace('&', 'and')

    start_time = time.time()
    replacements1 = ['!', '@', '$', '%', '^', '[', ']',
                     '{', '}', '\\', '|', '`', '~', '-', '=', '(', ')', '.']
    for replace1 in replacements1:
        full_text = full_text.replace(replace1, '')

    replacements1 = ['!', ',', '_', '/', ':', ';', '?', '<', '>']
    for replace1 in replacements1:
        full_text = full_text.replace(replace1, ' ')
    # create empty skills dictionary
    # if the skill exists in the job descriptions,
    # increment the frequency count in the dictionary
    # older code
    #     skill_dict = {}
    #     for word in skills:
    #         if ' ' + word.lower() + ' ' in full_text:
    #             if word in skill_dict:
    #                 skill_dict[word] += 1
    #             else:
    #                 skill_dict[word] = 1
    # older code end

    skills_raw = skills

    # data cleaning for skills
    start_time = time.time()
    skills = [x.lower() for x in skills]
    for i in range(len(skills)):
        skills[i] = skills[i].replace('&', 'and')
    replacements1 = ['!', '@', '$', '%', '^', '[', ']',
                     '{', '}', '\\', '|', '`', '~', '-', '=', '(', ')', '.']
    for i in range(len(skills)):
        for replace1 in replacements1:
            skills[i] = skills[i].replace(replace1, '')

    replacements1 = ['!', ',', '_', '/', ':', ';', '?', '<', '>']
    for i in range(len(skills)):
        for replace1 in replacements1:
            skills[i] = skills[i].replace(replace1, ' ')

    skills_truncated = []
    for i in range(len(skills)):
        skill = word_tokenize(skills[i])
        if len(skills[i]) > 5:
            skill = skill[0:5]
        skill = ' '.join(skill)
        skills_truncated.append(skill)
    skills = skills_truncated

    df = pd.DataFrame()
    df['skills_raw'] = skills_raw
    df['skills'] = skills

    start_time = time.time()

    skill_dict = {}
    for i in range(1, 3):
        for word in ngrams(full_text.split(), i):
            if i == 1:
                word = ''.join(word).lower()
            else:
                word = ' '.join(word).lower()
            if word in skill_dict:
                skill_dict[word] += 1
            else:
                skill_dict[word] = 1

    start_time = time.time()
    skill_dict = dict((key, value)
                      for key, value in skill_dict.items() if key in skills)
    print("lines 119", time.time() - start_time)

    start_time = time.time()
    temp_list = []
    for key, value in skill_dict.items():
        skill_raw = df[df['skills'] == key].iloc[0, 0]
        temp_list.append({'skill': skill_raw, 'value': value})
    skill_dict = temp_list

    return skill_dict


def get_top_ten_skills(jobs):
    skill_dict = extract_skills(jobs)
    sort_skills = sorted(skill_dict, key=lambda k: k['value'], reverse=True)
    top_10 = sort_skills[:30]
    return top_10
