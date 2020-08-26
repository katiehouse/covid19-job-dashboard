# import packages
import bs4
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

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
def extract_salary(div, full_text):
    try:
        return div.find("nobr").text
    except:
        try:
            span = div.find_all(name="span", attrs={"class": "salaryText"})
            return span[0].get_text()
        except:
            try:
                salary_text = full_text.find(text=re.compile("(\$)"), recursive=True)
                salary = re.search("\$[\d\.\,]+ to \$[\d\.\,]+ | \$[\d\.\,]+ - \$[\d\.\,]+, \$[\d\.\,]+/[\w]+ | \$[\d\.\,]+ per [\w]+", salary_text)
                return salary.group(0)
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


# extract job summary
def extract_summary(full_text):
    #assuming what we want will be early on
    try:
        summary_header = full_text.find("b", text=re.compile("(Summary|Description|Position|Role|Purpose|Overview)"), recursive=True)
        summary = ""
        if summary_header:
            #recursively search for next sibling, then parent and parents next siblig and so on
            return recursive_summary(summary_header)
        # if no key words are find, just return the first paragraph
        else:
            summary = full_text.findAll("p")
            index = 0
            while len(summary[index].text.split(" "))<10:
                index+=1
                if index < len(summary):
                    index-=1
                    break
            return summary[index].text
    except:
        return "NOT_FOUND"

    return "NOT_FOUND"


def recursive_summary (summary_header):
    summary = ""
    if summary_header.nextSibling:
        try:
            summary = summary_header.nextSibling.text
            #print("first try:", summary)
        except Exception as e:
            pass
    if summary.replace("/n", "").replace(" ", "") == "" or len(summary.split(" "))<10 :
        try:
        #    print("nextSibling", summary_header.nextSibling)
            return recursive_summary(summary_header.nextSibling)
        except:
        #    print("parent", summary_header.parent)
            return recursive_summary(summary_header.parent)
    else:
        return summary


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
def extract_fulltext(link):
    try:
        page = requests.get(link)
        soup = get_soup(page.text)
        spans = soup.find_all(name="div", attrs={"id": "jobDescriptionText"})
        for span in spans:
            return span
    except:
        return "NOT_FOUND"
    return "NOT_FOUND"


def scrape_indeed(input_dict, max_results_per_city = 2000):

    city = input_dict['zipcode']
    job_qry = input_dict['query']

    # file num
    file = 1

    # from where to skip
    SKIPPER = 0

    # # loop on all cities
    # for city in city_set:

        # # for each job role
        #for job_qry in job_set:

    # count
    cnt = 0
    startTime = time.time()

    # skipper
    if file > SKIPPER:

        # dataframe
        df = pd.DataFrame(
            columns=[
                "unique_id",
                "city",
                "job_qry",
                "job_title",
                "company_name",
                "location",
                "link",
                "date",
                "full_text",
                "salary",
                "summary"
            ]
        )

        link = (
            "http://www.indeed.com/jobs?q="
            + job_qry
            + "&l="
            + str(city)
            + "&radius=10&sort=date"
        )
        # get dom
        page = requests.get(link)

        # ensuring at least 1 second between page grabs
        time.sleep(1)

        # fetch data
        soup = get_soup(page.text)
        page.close()
        searchCountpages = soup.find_all(name="div", attrs={"id": "searchCountPages"})

        total_results = searchCountpages[0].get_text().strip().split(" ")[3]
        total_results = int(total_results.replace(",", ""))
        print("titalresults:", total_results)

        if total_results > max_results_per_city:
            total_results = max_results_per_city

        # for results
        for start in range(0, total_results, 10):
            link = (
                "http://www.indeed.com/jobs?q="
                + job_qry
                + "&l="
                + str(city)
                + "&start="
                + str(start)
                + "&radius=10&sort=date"
            )
            # print(link)
            print("Getting results %i out of %i" % (start, total_results))
            # get dom
            page = requests.get(link)

            # ensuring at least 1 second between page grabs
            time.sleep(1)

            # fetch data
            soup = get_soup(page.text)
            page.close()
            divs = soup.find_all(name="div", attrs={"class": "row"})

            # if results exist
            if len(divs) == 0:
                break

            # for all jobs on a page
            for div in divs:
                # specifying row num for index of job posting in dataframe
                num = len(df) + 1
                cnt = cnt + 1

                # job data after parsing
                job_post = []

                # append unique id
                job_post.append(div["id"])

                # append city name
                job_post.append(city)

                # append job qry
                job_post.append(job_qry)

                # grabbing job title
                job_post.append(extract_job_title(div))

                # grabbing company
                job_post.append(extract_company(div))

                # grabbing location name
                job_post.append(extract_location(div))

                # grabbing link
                link = extract_link(div)
                job_post.append(link)

                # grabbing date
                job_post.append(extract_date(div))

                # grabbing full_text
                full_text = extract_fulltext(link)
                job_post.append(full_text.text.strip())

                # grabbing salary
                job_post.append(extract_salary(div, full_text))

                # grabbing summary text
                job_post.append(extract_summary(full_text))

                # appending list of job post info to dataframe at index num
                df.loc[num] = job_post

        # will save to the database instead of json
        # df.to_json("indeed.json", orient='records')
        # df.to_csv("jobs_" + str(file) + ".csv", encoding="utf-8")
        return df.to_json(orient='records')

    else:

        # increment file
        file = file + 1

####################################
# COMMENT OUT EVERYTHING BELOW
# (used for local dev)
####################################

# #funct to see output-- saved in directory that repo is in.
# def write_logs(text):
#     # print(text + '\n')
#     f = open("../../log.json", "a")
#     f.write(text + "\n")
#     f.close()
#
# # to run script locally
# if __name__ == "__main__":
#     input = {'zipcode': 'Massachusetts', 'query': 'data'}
#     write_logs(scrape_indeed(input, max_results_per_city = 20))