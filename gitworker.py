import os

from git import Repo
import conf as conf
import mdworker as mdworker

git_repository = conf.config['git']["repository"]
git_working_dir = conf.config['git']["working_dir"]
git_username = conf.config['git']['username']
git_password = conf.config['git']['password']


def init():
    clone_repository()
    pull()


def get_remote():
    remote = f"https://{git_username}:{git_password}@github.com/{git_repository}"
    return remote


def clone_repository():
    if len(os.listdir(git_working_dir)) == 0:
        print("Cloning repository " + git_repository + " to directory " + git_working_dir)
        Repo.clone_from(get_remote(), git_working_dir)
        print("Succesfully cloned the repository")


def pull():
    print("Pulling latest changes")
    repo = Repo(git_working_dir)
    o = repo.remotes.origin
    o.pull()
    print("Pulled latest changes")


def do_pull_request():
    # do a basic commit on a sep. branch and then use the github specific code to create a PR for this commit
    print("od")


def commit_submission(submission):
    print("Making a commit for submission")

    # markdowner.create_markdown_file(submission)
    # transform submission title into a branch-name
    created_file = mdworker.create(submission)
    # new-submission: submission-title - automatically created by the list bot (huckleberry)
    repo = Repo(git_working_dir)
    repo.create_head("new_post_" + created_file["file_title"])
    repo.index.add(created_file["file_location_absolute"])
    repo.index.commit(
        "Automatically created from the-list-bot, added a new post with a slug of " + created_file["file_title"])

    for commit in list(repo.iter_commits()):
        print('COMMITS--->', commit.stats.files)

    origin = repo.remote(name="origin")
    origin.push()
    # create new branch
    # create markdown file
    # add changes
    # do commit
    # create pull request
    # return true
