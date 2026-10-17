# Python Job Tracker

A Python-based job tracking tool that collects remote job listings from
[We Work Remotely](https://weworkremotely.com/), stores them in a local
SQLite database, and sends email notifications when new listings match
your chosen keywords.

The goal is to make job searching easier by automatically gathering
listings and alerting you to opportunities that are relevant to your
interests.

## Features

-   **Automated job scraping** --- collects listings from We Work
    Remotely and its job categories.
-   **Job details extraction** --- records the job category, title,
    company, work type, pay information, location, and listing URL where
    available.
-   **SQLite storage** --- saves listings locally in `jobs.db`.
-   **Duplicate prevention** --- uses the job URL as a unique database
    field to avoid saving the same listing more than once.
-   **Keyword-based alerts** --- checks job titles against configurable
    keywords.
-   **Email notifications** --- emails a summary of new matching jobs.
-   **Scheduled checks** --- can run the tracker immediately and then
    repeat every six hours.

## Tech Stack

-   Python
-   SQLite (`sqlite3`)
-   `requests`
-   `BeautifulSoup` (`beautifulsoup4`)
-   `lxml`
-   `schedule`
-   Python's built-in `smtplib` and `email` modules

## Project Structure

``` text
Python-Job-Tracker/
├── main.py        # Coordinates scraping, database storage, and notifications
├── scraper.py     # Scrapes job listings from We Work Remotely
├── database.py    # Creates and interacts with the SQLite database
├── notifier.py    # Sends email alerts for matching new jobs
├── scheduler.py   # Runs the job check immediately and every six hours
├── config.py      # Local configuration (create this file; do not commit secrets)
├── jobs.db        # SQLite database created when the tracker runs
└── README.md
```

## Requirements

-   Python 3.9 or later is recommended.
-   An internet connection.
-   A Gmail account and an app password if you want to receive email
    alerts.

## Setup

### 1. Clone the repository

``` bash
git clone https://github.com/Ani-4a4/Python-Job-Tracker.git
cd Python-Job-Tracker
```

### 2. Create and activate a virtual environment (recommended)

**Windows (PowerShell):**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install requests beautifulsoup4 lxml schedule
```

### 4. Create your local configuration file

The project imports settings from `config.py`. Create this file in the
project directory and define the values used by the application:

``` python
# config.py

# Email settings used by notifier.py
EMAIL_FROM = "your_gmail_address@gmail.com"
EMAIL_TO = "recipient@example.com"
EMAIL_PASSWORD = "your_gmail_app_password"

# Job titles containing any of these words will trigger an email alert
NOTIFY_KEYWORDS = [
    "python",
    "developer",
    "software engineer",
    "backend",
    "data analyst",
]
```

Replace the example values with your own. `EMAIL_PASSWORD` should be a
**Gmail app password**, not your regular Gmail password. Gmail app
passwords require the relevant Google account security settings,
including two-step verification.

**Security:** Do not commit `config.py`, email passwords, or other
credentials to GitHub. Add `config.py` to `.gitignore` if it is not
already ignored. If a credential has been committed, revoke or rotate
it.

## Usage

### Run one job check

``` bash
python main.py
```

This runs the tracker once. It scrapes the listings, attempts to save
them to the database, identifies newly inserted jobs whose titles match
`NOTIFY_KEYWORDS`, and sends an email containing those matching jobs.

### Run continuously on a six-hour schedule

``` bash
python scheduler.py
```

The scheduler performs a check when it starts, then schedules another
check every six hours. Keep the process running for scheduled checks to
continue. Press `Ctrl + C` to stop it.

## How It Works

1.  **Scrape:** `scraper.py` requests the We Work Remotely website and
    parses job categories and listing details using BeautifulSoup.
2.  **Store:** `database.py` creates the SQLite `jobs` table if needed
    and inserts listings. The listing URL is unique, which helps prevent
    duplicate records.
3.  **Filter:** `main.py` checks the titles of newly inserted jobs
    against the configured notification keywords.
4.  **Notify:** `notifier.py` builds an email summary and sends it
    through Gmail's SMTP server over SSL.
5.  **Repeat:** `scheduler.py` runs the check on startup and every six
    hours while it remains running.

## Database

The default database file is `jobs.db`. The `jobs` table stores:

  Field         Description
  ------------- ------------------------------------------------
  `id`          Automatically generated record ID
  `job_type`    Category associated with the listing
  `title`       Job title
  `company`     Hiring company
  `work_type`   Employment type, when available
  `pay`         Pay information, when available
  `location`    Location information, when available
  `url`         Listing URL; unique to help prevent duplicates

The database is created locally when the application initializes. Back
up `jobs.db` if you want to preserve your collected listings.

## Notes and Limitations

-   The scraper depends on the current structure of We Work Remotely's
    website. If the site's HTML changes, the scraping logic may need to
    be updated.
-   Some listings may not include pay, location, or work-type details.
-   Email alerts depend on a valid Gmail configuration and network
    access.
-   Keyword matching is based on the job title. A listing is not alerted
    on simply because a keyword appears elsewhere in its description.
-   The scheduler only runs while the Python process is active.
-   This project is intended as a personal job-search aid; review the
    source site's terms and scraping policies before using it
    extensively.

## Future Improvements

Potential next steps include adding configurable job sources, richer
filtering, a command-line interface, automated tests, and more detailed
reporting.

## License

No license is specified here. Add a `LICENSE` file if you want to define
how others may use, modify, and distribute this project.
