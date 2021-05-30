import requests
from bs4 import BeautifulSoup

LIMIT = 10

def get_last_pages(URL):
 result = requests.get(URL)
 soup = BeautifulSoup(result.text, "html.parser")
 pagination = soup.find("div", {"class" : "pagination"})
 links = pagination.find_all('a')


 pages = []
 for link in links[:-1]:
  pages.append(int(link.string))
 max_pages = pages[-1]
 return max_pages

def extract_jobs(html):
   title = html.find("h2", {"class" : "title"})
   company =  html.find("span", {"class" : "company"}).text.strip("\n")
   titles = title.find("a", {"class" : "jobtitle turnstileLink"}).string
   location = html.find("span", {"class" : "location accessible-contrast-color-location"})
   locations = location.string
   job_id = html["data-jk"]
   return {'title':titles, 'company':company, 'location':locations, 'link': f"https://kr.indeed.com/jobs?q=python&vjk={job_id} "}

        
def extract_indeed_jobs(last_page, URL):
  jobs =[]
  for page in range(last_page):
   print(f"Scarpping page {page}")
   result = requests.get(f"{URL}start={page*LIMIT}")
   soup = BeautifulSoup(result.text, "html.parser")
   results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})
  try:
   results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})
  except AttributeError:
    pass

  for result in results:
   job = extract_jobs(result)
   jobs.append(job)
  return jobs

def get_jobs(word):
 URL = f"https://kr.indeed.com/jobs?q={word}&start="
 last_pages = get_last_pages(URL)
 jobs = extract_indeed_jobs(last_pages, URL)
 return jobs

