import os

from github import Github

token = os.environ["FAS_CONTENTS_GITHUB_TOKEN"]
g = Github(token)

# Then play with your Github objects:
for repo in g.get_user().get_repos(visibility="public"):
    print(repo.name)
