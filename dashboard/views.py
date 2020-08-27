from django.shortcuts import render
from services.scraper_service import *
import json
from services.location_service import *

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time


def progress_bar(seconds):
    progress_recorder = ProgressRecorder()
    result = 0
    for i in range(seconds):
        time.sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, seconds)
    return result

def jobs(request):
    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')
        query = request.POST.get('query')
    else:
        host = request.get_host()
        zipcode = get_city(host)
        query = 'Data Science'
    max_results = 20
    scrape_input = {'zipcode': zipcode, 'query': query}
    job_scaper = scrape_indeed.delay(scrape_input, max_results)
    print(job_scaper)
    jobs = json.loads(job_scaper.get())
    context = {'jobs': jobs, 'input': scrape_input}
    return render(request, '../templates/jobs.html', context)
