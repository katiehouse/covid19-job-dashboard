########################################################
# try filtering by linkedin skills
########################################################
import csv
import pandas as pd

with open('text_analysis/linked_in_skills.csv') as f:
    reader = csv.reader(f)
    skills = list(reader)

skills = [''.join(skill) for skill in skills] 

with open('text_analysis/indeed.json') as f:
        indeed = json.load(f)
indeed_df = pd.json_normalize(indeed)
full_text = indeed_df['full_text']

all_rows = []
for i in range(len(full_text)):
    row_temp = []
    for word in linkedin_skills:
        if word in full_text.iloc[0]:
            row_temp.append(word)
    all_rows.append(row_temp)