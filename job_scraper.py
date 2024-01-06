import requests
from bs4 import BeautifulSoup

import pandas as pd
import time
from datetime import datetime

def extract_job_title_from_result(div):
    job_title = div.find_all(name="a",attrs = {"data-tn-element":"jobTitle"})
    if len(job_title)>0:
        for a in job_title :
            return (a["title"])
    else:
        return "NOT_FOUND"

def extract_company_from_result(div): 
  company = div.find_all(name="span", attrs={"class":"company"})
  if len(company) > 0:
        return(company[0].text.strip())
  else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        return (span.text.strip())
      return 'NOT_FOUND'
 
def extract_salary_from_result(div): 
    salary = div.find_all(name="span", attrs={"class":"salary"})
    if len(salary) >0:
        return (salary[0].text.strip())
    else:
        return "NOT_FOUND"

def extract_link_from_result(div):
    link = div.find_all(name='a', attrs={'data-tn-element':'jobTitle'})
    if len(link) >0:
        for a in link:
            return(a['href'])
    else:
        return 'NOT_FOUND'

def extract_date_from_result(div):
    spans = div.find_all('span', attrs={'class':'date'})
    if len(spans) >0:
        return (spans[0].text.strip())
    else:
         return "NOT_FOUND"

max_results_per_city = 20
city_set = ['Toronto','Markham','Vancouver', 'Waterloo', 'North+York']
job_set = ['embedded+engineer', 'iot+engineer', 'firmware+engineer' ]
column = ["job_query","city", "job_title", "company_name", "salary","date", "link"]
sample_df = pd.DataFrame(columns = column)

def main():
    #finds jobs based on cities to work in and jobs the user wants
    for city in city_set:        
        for job in job_set:         
            for start in range(0, max_results_per_city, 10):
                    #get html from URL created using job and city 
                    page = requests.get("https://ca.indeed.com/jobs?q=" + job + "&l=" + str(city) + '&start=' + str(start))
                    time.sleep(1) 
                    soup = BeautifulSoup(page.text, "html.parser")
                    divs = soup.find_all(name="div", attrs={"class":"row"})
                    
                    #extract job details for each job on the page                    
                    for div in divs:           
                        num = (len(sample_df)+1)
                        job_post = [] 
                        job_post.append(job)
                        job_post.append(city) 
                        job_post.append(extract_job_title_from_result(div))
                        job_post.append(extract_company_from_result(div))      
                        job_post.append(extract_salary_from_result(div))
                        job_post.append(extract_date_from_result(div))
                        job_post.append( "https://www.indeed.com" +extract_link_from_result(div) )
                        sample_df.loc[num] = job_post
    
    #saves job posting in csv file 
    sample_df.to_csv('jobs_' +  datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv', encoding='utf-8')
    print("done")

if __name__ == "__main__":
    main()