from django.shortcuts import render
from services.scraper_service import *
import json
from services.location_service import *


def jobs(request):
    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')
        query = request.POST.get('query')
        max_results = 20
        input = {'zipcode': zipcode, 'query': query}
        jobs = json.loads(scrape_indeed(input, max_results))
        
    else:
        #host = request.get_host()
        #zipcode = get_city(host)
        zipcode = ""
        query = ""
        input = {'zipcode': zipcode, 'query': query}
        jobs = []
    context = {'jobs': jobs, 'input': input}
    return render(request, '../templates/jobs.html', context)
