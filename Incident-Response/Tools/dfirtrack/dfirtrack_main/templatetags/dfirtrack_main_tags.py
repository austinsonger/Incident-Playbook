from django import template
from git import Repo
from os import environ, getcwd

register = template.Library()

@register.simple_tag
def dfirtrack_version():
    versionnumber = 'v1.0.0'
    return versionnumber

"""
following conditions are necessary for Pull Requests

GitHub actions do some kind of `git checkout` on PRs, which causes
'TypeError: HEAD is a detached symbolic reference as it points to...'

multiple issues exists on this in https://github.com/gitpython-developers/GitPython
actually solved, but does still not work here
"""

# check for GitHub action
if not "CI" in environ:
    @register.simple_tag
    def dfirtrack_branch():
        # not in GitHub action --> get and return current branch
        working_dir = getcwd()
        repo = Repo(working_dir)
        branch = repo.active_branch
        return branch
else:
    @register.simple_tag
    def dfirtrack_branch():
        # in GitHub action --> return dummy value to avoid errors
        return "unknown"

# check for GitHub action
@register.simple_tag
def github_ci():
    if not "CI" in environ:
        # not in GitHub action --> show branch in maintemplate
        ci = False
    else:
        # in GitHub action --> do not show branch in maintemplate
        ci = True
    return ci
