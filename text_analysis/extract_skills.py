from csv import reader
from json import load
from pandas import json_normalize
from collections import Counter 
from nltk import ngrams
from nltk import word_tokenize

def extract_skills():
    # read in skills corpus
    with open('text_analysis/linked_in_skills.csv') as f:
        reader = csv.reader(f)
        skills = list(reader)

    # convert skills to list of strings
    skills = [''.join(skill) for skill in skills] 

    # read in .json
    with open('text_analysis/indeed.json') as f:
            indeed = json.load(f)
    indeed_df = json_normalize(indeed)

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
    
    replacements1 = ['!', '@','#','$','%','^','[',']','{','}','\\','|','`','~','-','=', '(', ')', '.']
    for replace1 in replacements1:
        full_text = full_text.replace(replace1, '')
    
    replacements1 = ['!', ',','_','/',':',';','?','<','>']
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

    skills = [x.lower() for x in skills]
    for i in range(len(skills)):
        skills[i] = skills[i].replace('&', 'and')
    replacements1 = ['!', '@','#','$','%','^','[',']','{','}','\\','|','`','~','-','=', '(', ')', '.']
    for i in range(len(skills)):
        for replace1 in replacements1:
            skills[i] = skills[i].replace(replace1, '')
    
    replacements1 = ['!', ',','_','/',':',';','?','<','>']
    for i in range(len(skills)):
        for replace1 in replacements1:
            skills[i] = skills[i].replace(replace1, ' ')
    
    skill_dict = {}
    for i in range(1,6):
        for word in ngrams(full_text.split(), i):
            if i == 1:
                word = ''.join(word).lower()
            else:
                word = ' '.join(word).lower()
            if word in skill_dict:
                skill_dict[word] += 1
            else:
                skill_dict[word] = 1
    
    
    skill_dict = dict((key,value) for key, value in skill_dict.items() if key in skills)
    
    temp_list = []
    for key, value in skill_dict.items():
        temp_list.append({'skill': key, 'value': value})
    skill_dict = temp_list

    return(skill_dict)

def main():
    skill_dict = extract_skills()
    sort_skills = sorted(skill_dict, key = lambda k:k['value'], reverse = True)
    top_10 = sort_skills[:10]
    print(top_10)


if __name__ == "__main__":
    main()
