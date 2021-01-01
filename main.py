import os
import praw
from tqdm import tqdm
import gitworker as gitworker
import redditworker as redditworker
import db as db





def find_callouts(submissions):
    for submission in tqdm(submissions):
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        for top_level_comment in comments:
            if top_level_comment.body.find("!addittothelist") != -1 or top_level_comment.body.find("!AITTL") != -1:
                handle_callout(submission, top_level_comment)
        print("------------------------------------------")


def handle_callout(submission, comment):
    print(f'handling a callout for submission {submission}')
    print(f'was requested in the comment {comment}')
    if db.check_submission(submission) > 0:
        print("already exists in db")
    else:
        print("does not exist yet, creating an in-progress record")
        db.create_record(submission, "in-progress")
        created_submission = gitworker.commit_submission(submission)
        if created_submission['status'] == 201:
            db.update_record(submission, "pull-requested")
            redditworker.reply_created_pr(comment, created_submission)
        else:
            db.update_record(submission, "already-exists")


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

    redditworker.loop_comments_stream(find_callouts)
