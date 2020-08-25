# import packages
import bs4
from bs4 import BeautifulSoup
import requests

# get soup object
def get_soup(text):
    return BeautifulSoup(text, "lxml")# , from_encoding="utf-8")


# extract company
def extract_company(div):
    company = div.find_all(name="span", attrs={"class": "company"})
    if len(company) > 0:
        for b in company:
            return b.text.strip()
    else:
        sec_try = div.find_all(name="span", attrs={"class": "result-link-source"})
        for span in sec_try:
            return span.text.strip()
    return "NOT_FOUND"


# extract job salary
def extract_salary(div):
    try:
        return div.find("nobr").text
    except:
        try:
            span = div.find_all(name="span", attrs={"class": "salaryText"})
            return span[0].get_text()
        except:
            return "NOT_FOUND"
    return "NOT_FOUND"


# extract job location
def extract_location(div):
    for span in div.findAll("span", attrs={"class": "location"}):
        if span.text != []:
            return span.text
        else:
            for span in div.findAll("div", attrs={"class": "location"}):
                return span.text
    return "NOT_FOUND"


# extract job title
def extract_job_title(div):
    for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
        return a["title"]
    return "NOT_FOUND"


# extract jd summary
def extract_summary(link):
    page = requests.get(link)
    soup = get_soup(page.text)
    spans = soup.find_all(name="div", attrs={"id": "jobDescriptionText"})
    for span in spans:
        return span.text.strip()
    return "NOT_FOUND"


# extract link of job description
def extract_link(div):
    try:
        return "https://www.indeed.com/viewjob?jk=" + div['data-jk']
    except:
        return "NOT_FOUND"


# extract date of job when it was posted
def extract_date(div):
    try:
        spans = div.findAll("span", attrs={"class": "date"})
        for span in spans:
            return span.text.strip()
    except:
        return "NOT_FOUND"
    return "NOT_FOUND"


# extract full job description from link
def extract_fulltext(url):
    try:
        page = requests.get("http://www.indeed.com" + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8") # got rid of warning: ("You provided Unicode markup but also provided a value for from_encoding. Your from_encoding will be ignored.")
        page.close()
        spans = soup.findAll("div", attrs={"class": "jobsearch-jobDescriptionText"})
        for span in spans:
            return span.text.strip()
    except:
        return "NOT_FOUND"
    return "NOT_FOUND"


# write logs to file
def write_logs(text):
    # print(text + '\n')
    f = open("log.txt", "a")
    f.write(text + "\n")
    f.close()