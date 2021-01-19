import os
from tqdm import tqdm
import gitworker as gitworker
import redditworker as redditworker
import db as db
import datetime, threading, time

next_call = time.time()


def check_on_prs():
    global next_call
    print("Checking on prs/comments")
    print(datetime.datetime.now())
    redditworker.check_callouts()
    next_call = next_call + 60
    threading.Timer(next_call - time.time(), check_on_prs).start()




def find_callouts(submissions):
    for submission in tqdm(submissions):
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        for top_level_comment in comments:
            if top_level_comment.body.find("!addittothelist") != -1 or top_level_comment.body.find(
                    "!AITTL") != -1 or top_level_comment.body.find("Get it on the list") != -1:
                handle_callout(submission, top_level_comment)
        print("------------------------------------------")


def handle_callout(submission, comment):
    print(f'handling a callout for submission {submission}')
    print(f'was requested in the comment {comment}')
    if db.check_submission(submission) > 0:
        print("already exists in db")
    else:
        print("does not exist yet, creating an in-progress record")
        db.create_record(submission, "in-progress", "", "")
        created_submission = gitworker.commit_submission(submission)
        if created_submission['status'] == 201:
            reply_id = redditworker.reply_created_pr(comment, created_submission)  # should return the comment id
            db.update_record(submission, "pull-requested", reply_id, created_submission['pr_id'])
        else:
            db.update_record(submission, "already-exists", "", "")


def create_directory(name):
    try:
        os.mkdir(name)
    except OSError:
        print("Creation of the directory %s failed" % name)
    else:
        print("Successfully created the directory %s " % name)


if __name__ == '__main__':
    try:
        file = open("init", 'r')
    except IOError:
        file = open("init", 'w')
        create_directory("db")  # sqlite file lives here
        create_directory("work")  # the-list repository lives here
        db.create_db()

    gitworker.init()
    check_on_prs()
    redditworker.loop_comments_stream(find_callouts)
