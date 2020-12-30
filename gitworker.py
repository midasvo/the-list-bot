import os

from git import Repo
import conf as conf
import mdworker as mdworker
import requests
import json
import time

git_repository = conf.config['git']["repository"]
git_working_dir = conf.config['git']["working_dir"]
git_username = conf.config['git']['username']
git_password = conf.config['git']['password']


def init():
    clone_repository()
    pull()


def get_remote():
    remote = f"https://{git_username}:{git_password}@github.com/{git_repository}" + ".git"
    return remote


def clone_repository():
    if len(os.listdir(git_working_dir)) == 0:
        print("Cloning repository " + git_repository + ".git to directory " + git_working_dir)
        Repo.clone_from(get_remote(), git_working_dir)
        print("Successfully cloned the repository")


def pull():
    print("Pulling latest changes")
    repo = Repo(git_working_dir)
    repo.git.checkout('main')
    o = repo.remotes.origin
    o.pull()
    print("Pulled latest changes")


def create_pull_request(branch_name, file_title):
    print("Creating a pull request for branch " + branch_name)

    token = "token " + git_password
    headers = {'Authorization': token}
    url = "https://api.github.com/repos/" + git_repository + "/pulls"
    title = "Add new submission  " + file_title + " from branch " + branch_name
    body = json.dumps({'title': title, 'head': branch_name, 'base': 'main'})
    r = requests.post(url, headers=headers, data=body)
    print(r.status_code, r.reason)
    if r.status_code == 201:
        return_obj = {
            'url': json.loads(r.text)['html_url']
        }
        return return_obj
        print("Successfully created the PR, found at " + json.loads(r.text)['html_url'])
    else:
        print("Encountered an error while creating the PR... " + r.reason)


def commit_submission(submission):
    pull()

    print("Making a commit for submission")
    branch_name = "new_submission_" + str(submission)
    repo = Repo(git_working_dir)
    origin = repo.remote(name="origin")
    repo.head.reference = repo.create_head(branch_name)

    created_file = mdworker.create(submission)

    repo.index.add(created_file["file_location_absolute"])
    repo.index.commit(
        "Automatically created from the-list-bot, added a new post with a slug of " + created_file["file_title"])
    origin.push(branch_name)
    print("Sleeping for 10 seconds before creating PR")
    time.sleep(10)
    pr = create_pull_request(branch_name, created_file['file_title'])
    return_obj = {
        'pr_url': pr['url'],
        'branch': branch_name
    }
    return return_obj
