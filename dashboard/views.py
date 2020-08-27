from django.shortcuts import render
from services.scraper_service import *
import json
import os
import psycopg2
from services.location_service import *
from .models import Query


def jobs(request):
    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')
        query = request.POST.get('query')
    else:
        host = request.get_host()
        zipcode = get_city(host)
        query = 'Data Science'
    max_results = 20
    input = {'zipcode': zipcode, 'query': query}
    jobs = json.loads(scrape_indeed(input, max_results))
    context = {'jobs': jobs, 'input': input}
    return render(request, '../templates/jobs.html', context)
