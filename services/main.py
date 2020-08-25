# import packages
import requests
import pandas as pd
import time
from functions import *


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
            write_logs(
                ("Completed =>")
                + "\t"
                + city
                + "\t"
                + job_qry
                + "\t"
                + str(cnt)
                + "\t"
                + str(start)
                + "\t"
                + str(time.time() - startTime)
                + "\t"
                + ("file_" + str(file))
            )

        # saving df as a local csv file
        df.to_json("indeed.json", orient='records')

        # df.to_csv("jobs_" + str(file) + ".csv", encoding="utf-8")

    else:

        # debug add
        write_logs(
            ("Skipped =>")
            + "\t"
            + city
            + "\t"
            + job_qry
            + "\t"
            + str(-1)
            + "\t"
            + str(-1)
            + "\t"
            + str(time.time() - startTime)
            + "\t"
            + ("file_" + str(file))
        )

        # increment file
        file = file + 1

if __name__ == "__main__":
    input = {'zipcode': 'Massachusetts', 'query': 'data'}
    scrape_indeed(input, max_results_per_city = 20)
