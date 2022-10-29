import base64
import os
import shutil
import urllib
from urllib.parse import urlparse

import markdown2
from bs4 import BeautifulSoup
from github import Github
from github.GithubException import UnknownObjectException

markdowner = markdown2.Markdown()

REPLACE_URLS = ["https://user-images.githubusercontent.com/", "https://github.com/"]


def is_replace_url(url):
    "URLが差し替え対象ならばTrueを返却する"
    for replace_url in REPLACE_URLS:
        if url.startswith(replace_url):
            return True
    return False


def replace_md(md):
    "マークダウンテキストのURLを差し替え先に変更する"
    for url in REPLACE_URLS:
        md = md.replace(url, "https://fas-contents.web.app/")
    return md


def download_image(md):
    "README.md内で使われている画像をダウンロードする"
    html = markdowner.convert(md)
    soup = BeautifulSoup(html, "html.parser")
    for img in soup.find_all("img"):
        url = img.attrs.get("src")
        if is_replace_url(url):
            o = urlparse(url)
            os.makedirs("public%s" % (os.path.dirname(o.path)), exist_ok=True)
            try:
                image_data = urllib.request.urlopen(url).read()
                with open("public%s" % o.path, mode="wb") as f:
                    f.write(image_data)
            except urllib.error.HTTPError:
                pass


shutil.rmtree("public", ignore_errors=True)

token = os.environ["FAS_CONTENTS_GITHUB_TOKEN"]
g = Github(token)

for repo in g.get_user().get_repos(visibility="public"):
    os.makedirs("public/%s" % (repo.name), exist_ok=True)
    try:
        file = repo.get_readme()
        md = base64.b64decode(file.content).decode("utf-8")
        download_image(md)
        md = replace_md(md)
        with open("public/%s/README.md" % (repo.name), "w") as f:
            f.write(md)
    except UnknownObjectException:
        pass
