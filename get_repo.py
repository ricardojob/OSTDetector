# import pydriller
from pydriller import Repository
from pydriller import Git
import os

class Local:
    def __init__(self, dir):
        self.dir_local = dir
    
    def commit_head(self)-> str:
        gr = Git(self.dir_local)
        return gr.get_head().hash
    
    def path(self):
        return self.dir_local
        
class Repo:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def clone_at(self, dir) -> Local:
        local = Local(dir)
        repo = Repository(self.url,  clone_repo_to=dir)
        if not os.path.exists(dir):
            repo._clone_remote_repo(repo=self.url, tmp_folder=dir)
        return local
    
    def repo_name(self):
        return self.name
        
if __name__ == '__main__':
    dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/data/django/django'
    url = 'https://github.com/django/django'
    repo = Repo(url)
    local = repo.clone_at(dir)
    print(local.commit_head())