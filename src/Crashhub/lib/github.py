from github import Github
from github.GithubObject import NotSet

from flask import current_app, g

class GithubAppCtxWrapper:
    def init_app(self, app_context):
        self.app = app_context

gh_crash = GithubAppCtxWrapper()

def get_github():
    if 'github' not in g:
        github = Github(current_app.config.get("GITHUB_TOKEN"))
        g.github = github.get_repo(current_app.config.get("GITHUB_PROJECT"))
    return g.github

def report_issue(title, body):
    repo = get_github()
    issue = repo.create_issue(title, body)
    return issue.number


def update_issue(id, body):
    repo = get_github()
    repo.get_issue(id).edit(body=body)
    return id


def issue_is_closed(id):
    repo = get_github()
    closed_by = repo.get_issue(id).closed_by
    return closed_by is not NotSet and closed_by is not None and hasattr(closed_by, "login")


def issue_closed_by(id):
    repo = get_github()
    return repo.get_issue(id).closed_by


def respond(id, body):
    repo = get_github()
    repo.get_issue(id).create_comment(body)

