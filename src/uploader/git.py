from github import Github
from github import Auth
from github import Repository


from constants.credentials import GH_TOKEN, GH_REPO

auth = Auth.Token(GH_TOKEN)
gh_client = Github(auth=auth)

repo = gh_client.get_user().get_repo(GH_REPO)
