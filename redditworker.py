import praw
import conf as conf
import db as db
import gitworker as gitworker


def get_reddit():
    return praw.Reddit(user_agent=conf.config["reddit"]["user_agent"],
                       client_id=conf.config["reddit"]["client_id"],
                       client_secret=conf.config["reddit"]["client_secret"],
                       username=conf.config["reddit"]["username"],
                       password=conf.config["reddit"]["password"])


def loop_comments_stream(callback):
    subreddit = conf.config['reddit']['sub']
    print(f'Getting the comments stream of /r/{subreddit} \n')
    print("------------------------------------------")
    reddit = get_reddit()
    sub = reddit.subreddit(subreddit)
    callback(sub.stream.submissions())


def check_callouts():
    print("checking callouts")
    records = db.get_pull_requested_records()
    for record in records:
        submission = record[0]
        reply_id = record[2]
        pr_number = record[3]
        comment_score = get_comment_score(reply_id)
        if comment_score > 50:
            print("Reached the threshold of 50 score, merging the PR!")
            gitworker.accept_pull_request(pr_number)
            update_reply_pr_merged(reply_id)
            db.update_status(submission, "merged")
        else:
            print("Did not reach the threshold of 50 score, not merging the PR, the score is: " + str(comment_score))


def reply_created_pr(comment, created_submission):
    print("Replying to a comment")
    print(comment)
    with open('archetype/reply_created_pr') as f:
        s = f.read()
        print(s)
    s = s.replace("!!PR_URL!!", created_submission['pr_url'])
    print(s)
    reply = comment.reply(s)
    return reply.name


def update_reply_pr_merged(reply_id):
    reddit = get_reddit()
    comment = reddit.comment(reply_id)
    body = comment.body
    with open('archetype/reply_pr_merged') as f:
        s = f.read()
    comment.edit(body + s)
    db


def get_comment_score(comment_id):
    reddit = get_reddit()
    comment = reddit.comment(comment_id)
    parent = comment.parent()
    score = parent.score
    return score
