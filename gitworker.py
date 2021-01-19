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
    response_json = json.loads(r.text)
    if 'html_url' in response_json:
        url = response_json['html_url']
    else:
        url = ""

    if 'number' in response_json:
        number = response_json['number']
    else:
        number = ""
    return_obj = {
        'status': r.status_code,
        'reason': r.reason,
        'url': url,
        'number': number
    }
    return return_obj


def accept_pull_request(pr_number):
    print("Accepting pull request for " + pr_number)
    token = "token " + git_password
    headers = {'Authorization': token}
    url = "https://api.github.com/repos/" + git_repository + "/pulls/" + pr_number + "/merge"
    commit_title = "ListBot Automatically merged PR"
    body = json.dumps({'commit_title': commit_title})
    r = requests.put(url, headers=headers, data=body)
    print(r.status_code, r.reason)
    response_json = json.loads(r.text)
    return r.status_code


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
        'pr_id': pr['number'],
        'branch': branch_name,
        'status': pr['status']
    }
    return return_obj
