#Add all the preset skill to the database.
import csv
import string
from django.shortcuts import render
from .models import Skill    # Skill is the model class defined in models.py


#input_csv = "/Users/mm20264/Documents/Projects/ddfg2020/covid19-job-dashboard/services/linked_in_skills.csv"

def insert_skill(input_csv):
    """
    Take input as a csv file of. Add all skills to the database
    """

    rows = [] 
  
    # reading csv file 
    with open(input_csv, 'r') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
    
        # extracting each data row one by one 
        for row in csvreader: 
            rows.append(row)

    for i in range(len(rows)):
        current_lower = rows[i][0].lower()
        Skill.objects.create(skill_name = current_lower)

