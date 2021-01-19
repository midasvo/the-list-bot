import sqlite3
import conf as conf

sqlite_location = conf.config['db']['sqlite_location']


def create_db():
    print("Creating database at " + sqlite_location)
    conn = sqlite3.connect(sqlite_location)
    c = conn.cursor()
    c.execute('''CREATE TABLE submissions
                 (submission text, status text, comment_id text, pr_number text)''')
    conn.commit()
    conn.close()
    print("Done creating database")


def check_submission(submission):
    conn = sqlite3.connect(sqlite_location)
    c = conn.cursor()
    c.execute(f"SELECT COUNT(Submission) FROM submissions WHERE submission = ?", [str(submission)])
    is_new = c.fetchone()[0] != 0
    conn.close()
    return is_new


def create_record(submission, status, comment_id, pr_number):
    print("Creating a new record for " + str(submission))
    conn = sqlite3.connect(sqlite_location)
    c = conn.cursor()
    c.execute("INSERT INTO submissions (submission, status) "
              "VALUES (?, ?)",
              (str(submission), status))
    conn.commit()
    conn.close()
    print("Done creating record")


def update_record(submission, status, comment_id, pr_number):
    print("Updating record " + str(submission) + " and giving it a status of " + str(status))
    print("Creating a new record for " + str(submission))
    conn = sqlite3.connect(sqlite_location)
    c = conn.cursor()
    c.execute("UPDATE submissions SET status = ?, comment_id = ?, pr_number = ? WHERE submission = ?",
              (status, comment_id, pr_number, str(submission)))
    conn.commit()
    conn.close()
    print("Done creating record")


def update_status(submission, status):
    print("Updating record " + str(submission) + " and giving it a status of " + str(status))
    conn = sqlite3.connect(sqlite_location)
    c = conn.cursor()
    c.execute("UPDATE submissions SET status = ? WHERE submission = ?",
              (status, str(submission)))
    conn.commit()
    conn.close()


def get_pull_requested_records():
    conn = sqlite3.connect(sqlite_location)
    c = conn.cursor()
    c.execute("SELECT * FROM submissions WHERE status = 'pull-requested'")
    records = c.fetchall()
    conn.close()
    return records
