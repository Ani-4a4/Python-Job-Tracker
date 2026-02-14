import sqlite3

class JobDatabase():
    def __init__(self, db = 'jobs.db'):
        self.db = db
        self.Create_Table()

    def Create_Table(self):
        # Create jobs table if it does not exist
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       job_type TEXT,
                       title TEXT,
                       company TEXT,
                       work_type TEXT,
                       pay TEXT,
                       location TEXT,
                       url TEXT UNIQUE  
                       )''')
        conn.commit()
        conn.close()
        print('Database table has been created')

    def add_job(self, job_list):
        # Add new job to database
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        try:
            cursor.execute('''INSERT INTO jobs (
                        job_type, title, company, work_type, pay, location, url)
                        VALUES (?,?,?,?,?,?,?)''', (
                            job_list.get('job_type'),
                            job_list['title'],
                            job_list['company'],
                            job_list.get('work_type','Not specified'),
                            job_list.get('pay','Not specified'),
                            job_list.get('location','Not specified'),
                            job_list['url']
                        ))
            conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            return False
        
        finally:
            conn.close()

    def get_jobs(self, status = None):
        # Return a list of dictionaries of jobs depending on the status of the job
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if status:
            cursor.execute('SELECT * FROM jobs WHERE status = ?',(status,))
        else:
            cursor.execute('SELECT * FROM jobs')

        rows = cursor.fetchall()
        conn.close()

        jobs = [dict(row) for row in rows]
        return jobs


    def get_stats(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        # Total number of jobs
        cursor.execute('SELECT COUNT(*) FROM jobs')
        total = cursor.fetchone()[0]

        # Total number of jobs depending on status
        cursor.execute('SELECT COUNT(*) FROM jobs GROUP BY status')
        by_status = cursor.fetchall()

        # Total number of jobs depending on category
        cursor.execute('SELECT COUNT(*) FROM jobs GROUP BY job_type')
        by_category = cursor.fetchall()

        conn.close()

        return {
            'total':total,
            'by_status':by_status,
            'by_category':by_category
        }
    
    def delete_jobs(self, job_id):
        # Delete jobs from database depending on job_id
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM jobs WHERE id = ?',(job_id,))
        conn.commit()
        conn.close()
        print(f'Deleted job -> {job_id} successfully')




