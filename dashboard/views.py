from django.shortcuts import render
from services.scraper_service import *
import json
from services.location_service import *
from text_analysis.extract_skills import get_top_ten_skills


def jobs(request):
    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')
        query = request.POST.get('query')
        max_results = 20
        input = {'zipcode': zipcode, 'query': query}
        jobs = json.loads(scrape_indeed(input, max_results))
        skills = get_top_ten_skills(jobs)
        show = False
    else:
        #host = request.get_host()
        #zipcode = get_city(host)
        zipcode = ""
        query = ""
        input = {'zipcode': zipcode, 'query': query}
        jobs = None
        skills = []
        show = True
    
    context = {'jobs': jobs, 'input': input, 'skills': skills, 'show': show}
    return render(request, '../templates/jobs.html', context)