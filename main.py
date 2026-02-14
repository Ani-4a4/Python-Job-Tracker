from scraper import WebScraper
from database import JobDatabase
from config import NOTIFY_KEYWORDS
from notifier import JobNotifier

def matching_words(job):
    title = job['title'].lower()
    return any(keyword in title for keyword in NOTIFY_KEYWORDS)

def job_check():
    scraper = WebScraper('https://weworkremotely.com/')
    db = JobDatabase()
    notifier = JobNotifier()

    print(f'Scraping jobs')
    scraped_jobs = scraper.scrape_homepage()

    if not scraped_jobs:
        print('No jobs have been scraped') 
    
    print(f'Adding {len(scraped_jobs)} jobs to the database')
    new = 0
    duplicate = 0
    new_jobs = []
    for job in scraped_jobs:
        job_added = db.add_job(job)

        if job_added:
            new +=1
            print(f"Job {job['title']} at {job['company']} added")

            if matching_words(job):
                new_jobs.append(job)
        else:
            duplicate += 1

    if new_jobs:
        notifier.new_job_alert(new_jobs)


    print(f'Number of new jobs -> {new}')
    print(f'Number of duplicate jobs -> {duplicate}')

    # stats = db.get_stats()
    # print(f'Total number of jobs -> {stats["total"]}')

    # for category, count in stats["by_category"]:
    #     print(f'{category}:{count}')

if __name__ == "__main__": 
    job_check()
    