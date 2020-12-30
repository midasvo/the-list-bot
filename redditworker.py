
def reply_created_pr(comment, created_submission):
    print("Replying to a comment")
    print(comment)
    comment.reply("Hey you son of a bitch I just created a PR for you :) " + created_submission['pr_url'])
    print(created_submission)
