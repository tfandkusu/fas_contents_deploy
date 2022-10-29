import base64
import os
import shutil

from github import Github
from github.GithubException import UnknownObjectException

shutil.rmtree("public", ignore_errors=True)

token = os.environ["FAS_CONTENTS_GITHUB_TOKEN"]
g = Github(token)

for repo in g.get_user().get_repos(visibility="public"):
    os.makedirs("public/%s" % (repo.name), exist_ok=True)
    try:
        file = repo.get_readme()
        content = base64.b64decode(file.content)
        with open("public/%s/README.md" % (repo.name), "wb") as f:
            f.write(content)
    except UnknownObjectException:
        pass
