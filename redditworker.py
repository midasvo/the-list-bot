
def reply_created_pr(comment, created_submission):
    print("Replying to a comment")
    print(comment)
    with open('archetype/reply_created_pr') as f:
        s = f.read()
        print(s)
    s = s.replace("!!PR_URL!!", created_submission['pr_url'])
    print(s)
    comment.reply(s)
