import praw
import conf as conf


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


def reply_created_pr(comment, created_submission):
    print("Replying to a comment")
    print(comment)
    with open('archetype/reply_created_pr') as f:
        s = f.read()
        print(s)
    s = s.replace("!!PR_URL!!", created_submission['pr_url'])
    print(s)
    comment.reply(s)
