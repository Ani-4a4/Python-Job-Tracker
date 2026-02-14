from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests


class WebScraper():
    def __init__(self, url):
        self.url = url

    def scrape_homepage(self):
        url = self.url
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
        try:
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f'Error, status code: {response.status_code}')

            soup = BeautifulSoup(response.text, 'lxml')

            job_types = soup.find_all('h2')
            job_list = []
            
            for h2 in job_types:
                a_tag = h2.find('a')
                job_type = a_tag.text.strip()

                if a_tag:
                    follow_url = a_tag.get('href')
                    new_url = urljoin(self.url, follow_url)

                    print(f'Category:{job_type}, following the link - {new_url}')
                    category_jobs = self.scrape_categorypage(new_url, job_type)
                    job_list.extend(category_jobs)
                    print(f'Successfully added {len(category_jobs)} jobs from {job_type}.')

            return job_list

        except Exception as e:
            print(e)
        return job_list



    def scrape_categorypage(self,new_url,job_type):
        try:
            headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
            new_response = requests.get(new_url, headers=headers)

            if new_response.status_code != 200:
                print(f'Error, status code: {new_response.status_code}')

            soup = BeautifulSoup(new_response.text,'lxml')

            jobs = soup.find_all('li',class_='new-listing-container')
            job_list = []
            print(f'Scraping {len(jobs)} jobs')
            for li in jobs:
                try:

                    # Job title
                    title = li.find('h3', class_='new-listing__header__title').text.strip() 

                    # Hiring company
                    company = li.find('p', class_='new-listing__company-name').text.strip()

                    # Job url
                    link_tag = li.find('a')
                    if link_tag and link_tag.get('href'):
                        job_url = urljoin(self.url, link_tag.get('href'))
                    else:
                        job_url = new_url

                    pay = 'Not specified'
                    location = 'Not specified'
                    work_type = 'Not specified'
                    work_type_keywords = ["Full-Time", "Part-Time", "Contract", "Freelance", "Internship"]
                    tags = li.find_all('p', class_='new-listing__categories__category')

                    for tag in tags:
                        text = tag.text.strip()

                        # Pay
                        if 'USD' in text:
                            pay = text

                        # Work type
                        elif text in work_type_keywords:
                            work_type = text

                        # Location
                        else:
                            location = text

                    job = {
                        'job_type': job_type,
                        'title': title,
                        'company': company,
                        'work_type': work_type,
                        'pay': pay,
                        'location': location,
                        'url': job_url
                    }

                    job_list.append(job)
            
                except Exception as e:
                    continue

            return job_list

        except Exception as e:
            print(e)
            return []

        ''''
        First find the name of each type of Job -> from the homepage {Normal url}
        If view all link exists -> follow the link and scrape that page
        Use dictionary to save title, location, pay etc
        Else just scrape the home page for that section
        '''

# url = 'https://weworkremotely.com/'
# scraper = WebScraper(url)
# all_jobs = scraper.scrape_homepage()
# print(f'Total number of jobs scraped -> {len(all_jobs)}')
