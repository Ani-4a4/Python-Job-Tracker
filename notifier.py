import smtplib
from email.message import EmailMessage
from config import EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO

class JobNotifier():
    def __init__(self):
        self.from_email = EMAIL_FROM
        self.to_email = EMAIL_TO
        self.email_password = EMAIL_PASSWORD

    def new_job_alert(self, new_jobs):
        if not new_jobs:
            print('No new jobs to notify')
            return
        
        subject = f'{len(new_jobs)} new jobs have been found'
        body = f'The tracker has found {len(new_jobs)} new job(s) from the selected criteria'

        for i,job in enumerate(new_jobs,1):
            body += f"{i}.  Job_type: {job['job_type']}\n"
            body += f"      Title: {job['title']}\n"
            body += f"      Company: {job['company']}\n"
            body += f"      Work_type: {job['work_type']}\n"
            body += f"      Pay: {job['pay']}\n"
            body += f"      Location: {job['location']}\n"
            body += f"      URL: {job['url']}\n\n"

        self.send_email(subject,body)


    def send_email(self, subject, body):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg.set_content(body)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(self.from_email, self.email_password)
                smtp.send_message(msg)
                print(f'Email has been successfuly sent from {self.from_email}')
        except Exception as e:
            print(f'Failed to send email: {e}')

if __name__ == "__main__":
    notifier = JobNotifier()
    
    # Test email
    test_jobs = [
        {
            'job_type': 'Programming',
            'title': 'Python Developer',
            'company': 'TechCorp',
            'work_type': 'Full-Time',
            'pay': '$100k USD',
            'location': 'Remote',
            'url': 'https://example.com/job1'
        }
    ]
    
    notifier.new_job_alert(test_jobs)