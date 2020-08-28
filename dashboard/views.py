from django.shortcuts import render
from services.scraper_service import *
import json
from services.location_service import *
from text_analysis.extract_skills import get_top_ten_skills
import time


def jobs(request):
    if request.method == 'POST':
        startTime = time.time()
        zipcode = request.POST.get('zipcode')
        query = request.POST.get('query')
        max_results = 10
        input = {'zipcode': zipcode, 'query': query}
        jobs = json.loads(scrape_indeed(input, max_results))
        print("Time to get job results: ", time.time() - startTime)
        skills = get_top_ten_skills(jobs)
        print("Time to get skills: ", time.time() - startTime)
        number_of_jobs = len(jobs)
    else:
        #host = request.get_host()
        #zipcode = get_city(host)
        zipcode = ""
        query = ""
        input = {'zipcode': zipcode, 'query': query}
        jobs = []
        skills = []
        number_of_jobs = 0

    context = {'jobs': jobs, 'input': input, 'skills': skills,
               'number_of_jobs': number_of_jobs}
    return render(request, '../templates/jobs.html', context)
