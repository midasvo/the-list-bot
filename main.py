import praw
from tqdm import tqdm
import db as db
import gitworker as gitworker
import conf as conf


def get_reddit():
    return praw.Reddit(user_agent=conf.config["reddit"]["user_agent"],
                       client_id=conf.config["reddit"]["client_id"],
                       client_secret=conf.config["reddit"]["client_secret"],
                       username=conf.config["reddit"]["username"],
                       password=conf.config["reddit"]["password"])


def read_comments_stream():
    subreddit = conf.config['reddit']['sub']
    print(f'Getting the comments stream of /r/{subreddit} \n')
    print("------------------------------------------")
    reddit = get_reddit()
    sub = reddit.subreddit(subreddit)
    find_callouts(sub.stream.submissions())


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
        gitworker.commit_submission(submission)
        db.create_record(submission, "in-progress")


if __name__ == '__main__':
    try:
        file = open("init", 'r')
    except IOError:
        file = open("init", 'w')
        db.create_db()
    gitworker.init()

    read_comments_stream()
    # get top-level comments that call out bot -> done
    # retrieve the submission and specific comment -> done
    # check if submission is not already in file/sqlite
    # add the submission tag to a file/sqlite db with a status, e.g. in-progress
    # create a markdown post based on the submission
    # create a PR with the markdown post
    # reply to the comment saying whats what and link the PR
