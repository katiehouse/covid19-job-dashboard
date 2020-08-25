# import packages
import bs4
from bs4 import BeautifulSoup
import requests
import requests
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


# commented this out so we can use regular logs
# write logs to file
# def write_logs(text):
#     # print(text + '\n')
#     f = open("log.txt", "a")
#     f.write(text + "\n")
#     f.close()


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
                "summary",
                "salary",
                "date",
                "full_text",
            ]
        )

        link = (
            "http://www.indeed.com/jobs?q="
            + job_qry
            + "&l="
            + str(city)
            + "&radius=10&sort=date"
        )
        print(link)
        # get dom
        page = requests.get(link)

        # ensuring at least 1 second between page grabs
        time.sleep(1)

        # fetch data
        soup = get_soup(page.text)
        page.close()
        searchCountpages = soup.find_all(name="div", attrs={"id": "searchCountPages"})
        print(searchCountpages)

        total_results = searchCountpages[0].get_text().strip().split(" ")[3]
        total_results = int(total_results.replace(",", ""))

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

                # grabbing summary text
                job_post.append(extract_summary(link))

                # grabbing salary
                job_post.append(extract_salary(div))

                # grabbing date
                job_post.append(extract_date(div))

                # grabbing full_text
                job_post.append(extract_fulltext(link))

                # appending list of job post info to dataframe at index num
                df.loc[num] = job_post

            # debug add
            # write_logs(
            #     ("Completed =>")
            #     + "\t"
            #     + city
            #     + "\t"
            #     + job_qry
            #     + "\t"
            #     + str(cnt)
            #     + "\t"
            #     + str(start)
            #     + "\t"
            #     + str(time.time() - startTime)
            #     + "\t"
            #     + ("file_" + str(file))
            # )

        # saving df as a local csv file
        # will save to the database instead of json
        # df.to_json("indeed.json", orient='records')
        # df.to_csv("jobs_" + str(file) + ".csv", encoding="utf-8")
        return df.to_json(orient='records')

    else:

        # debug add
        # write_logs(
        #     ("Skipped =>")
        #     + "\t"
        #     + city
        #     + "\t"
        #     + job_qry
        #     + "\t"
        #     + str(-1)
        #     + "\t"
        #     + str(-1)
        #     + "\t"
        #     + str(time.time() - startTime)
        #     + "\t"
        #     + ("file_" + str(file))
        # )

        # increment file
        file = file + 1

# commented this out and moved everything to one generic scraper_service
# if __name__ == "__main__":
#     input = {'zipcode': 'Massachusetts', 'query': 'data'}
#     scrape_indeed(input, max_results_per_city = 20)
