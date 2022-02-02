url = "https://github.com/snathan-vaneck/R_Shiny_App2.git"

import os

print(os.system('ls -ltr'))
print(os.system('git clone {}'.format(url)))

from git import Repo
# repo = Repo(url)
# # assert not repo.bare
# rw_dir = "~/my_work/docker_django/configuration/mainapp"
# cloned_repo = repo.clone(os.path.join(rw_dir, './'))
# assert cloned_repo.__class__ is Repo     # clone an existing repository
# assert Repo.init(os.path.join(rw_dir, './')).__class__ is Repo
# Repo.clone_from(url, 'git_clone')
import git
git.Git("/home/finflock/my_work/docker_django/configuration/git_clone").clone(url)


