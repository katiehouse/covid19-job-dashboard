# import packages
import bs4
from bs4 import BeautifulSoup, NavigableString
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
            return span[0].get_text().replace("\n", "")
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
            summary = recursive_summary(summary_header)
        # if no key words are find, just return the first paragraph
        else:
            paragraphs = full_text.findAll("p")
            index = 0
            for paragraph in paragraphs:
                if len(paragraph.text.split(" "))>20:
                    summary = paragraph.text
                    break
            if not summary:
                summary = full_text.text
    except:
        try:
            summary = full_text.text
        except:
            return ""

    if len(summary)<300:
        return summary.replace("\n", " ")
    else:
        return summary[:300].replace("\n", " ") + "..."


def recursive_summary (summary_header):
    summary = ""
    if summary_header.nextSibling:
        try:
            summary = summary_header.nextSibling.text
        except Exception as e:
            pass
    if summary.replace("/n", "").replace(" ", "") == "" or len(summary.split(" "))<10 :
        try:
            return recursive_summary(summary_header.nextSibling)
        except:
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

def extract_skills(full_text):
    skills = []
    try:
        # identify headers - first look for <b> and then any tag as a backup

        header_regex = re.compile("(Skills|Qualifications|Requirements|ideal candidate|someone who|Experience|Aptitude|bring|What does it take)", re.IGNORECASE)

        skill_header = full_text.find_all("b", text=header_regex, recursive=True)
        if not skill_header:
            skill_header = full_text.find_all("p", text=header_regex, recursive=True)

        # for each header, if it's shorter than a paragraph, assume its a valid header and extract the corresponding list of skills, if it is a paragraph, assume it contains the skills
        for sub_header in skill_header:
            # print('sub_header', sub_header.text)
            if len(sub_header.text.split(' ')) < 10:
                skill_list = extract_list(sub_header)
                # print('extracted list (result):', skill_list)
                skills.append(', '.join(skill_list))

            if len(skills) == 0:
                # print('no skills extracted, using', sub_header)
                skills.append(sub_header.text)

        print('extracted skills:', skills)
        return(skills)
    except Exception as e:
        # print('exception in extract_skills/try:, returning NOT_FOUND')
        return "NOT_FOUND"

    # print('got past try/except somehow, returning NOT_FOUND')
    return "NOT_FOUND"

def extract_list(list_header, recursed = 0): # pulls a list given a header - the list can be a sibling or contained within a parent, and can include a single <ul>, many <ul> that each include <li>, or several <li>
    extracted_list = []
    # print('extracting_list for', list_header)
    try:
        next = list_header.nextSibling
        end = False
        while next and end == False: # step through siblings of the header
            # if not isinstance(next, NavigableString):

            if isinstance(next, NavigableString):
                # print('sibling: NavigableString:', str(next))
                pass
            else:
                # print('sibling:', next.name, next.text)

                if next.name == 'ul': # if it's an unordered list (ul), identify the list items (li) and add each to the extracted list
                    try: # case: each <ul> includes several <li>s
                        ul_li_items = next.find_all('li')
                        # print('ul items:', ul_li_items, ', length', len(ul_li_items))
                        for item in ul_li_items:
                            extracted_list.append(item.text)
                            # print('added li', item.text)
                    except: # case: there is a <ul> but it doesn't inclue list items, i.e. each sibling is a single item in the list
                        # print('no li items in list')
                        extracted_list.append(next.text)

                if next.name == 'p' or next.name == 'div':
                    extracted_list.append(next.text)
                    # print('added p or div', next.text)

            next = next.nextSibling # step forward

            # end condition for siblings
            if next and not isinstance(next, NavigableString):
                next_header_regex = re.compile("Job Type|Benefit|Education|Company|Authorization|Location|Offer|\.com|Responsibilities|About|Compensation", re.IGNORECASE)
                if next.name == 'b' or re.search(next_header_regex, next.text) or end == True: # assume this is the next header
                    end = True
                    # print('end stepping thru siblings (found header):', next.text)

        # print('while loop over')

        if len(extracted_list) > 0: # after while ends
            return(extracted_list)
        elif len(extracted_list) == 0 and recursed < 3:
            # print('no extracted list from ', list_header, ', recursing parent')
            return(extract_list(list_header.parent, recursed = recursed + 1))

    except Exception as e:
        print(e)
        parent = list_header.parent
        # print('exception in extract_list/try')
        if len(skills) == 0:
            # print('exception in while and no skills, recursing parent'
            return(extract_list(list_header.parent, recursed = recursed + 1))


        #print('Exception, checking parent')
        #return(extract_list(parent))
# end extract_list


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
                "summary",
                "skills",
                "total_jobs"
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
        print("total results:", total_results)

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

            #print("Getting results %i out of %i" % (start, total_results))
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
                print('\n', link)

                # grabbing date
                job_post.append(extract_date(div))

                # grabbing full_text
                full_text = extract_fulltext(link)
                try:
                    job_post.append(full_text.text.strip())
                except:
                    job_post.append(full_text)

                # grabbing salary
                job_post.append(extract_salary(div, full_text))

                # grabbing summary text
                summary = extract_summary(full_text)
                job_post.append(summary) #extract_summary(full_text))

                # grabbing skills
                job_post.append(extract_skills(full_text))

                # grabbing number of results for the whole search
                job_post.append(total_results)

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

#funct to see output-- saved in directory that repo is in.
def write_logs(text):
    f = open("../log.json", "a")
    f.write(text + "\n")
    f.close()

# to run script locally
if __name__ == "__main__":
    input = {'zipcode': 'Massachusetts', 'query': 'data'}
    write_logs(scrape_indeed(input, max_results_per_city = 10))
