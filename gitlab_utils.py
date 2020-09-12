from functools import lru_cache

import gitlab
from gitlab.v4.objects import Project


@lru_cache(maxsize=None)
def get_gitlab(url, api_token, verifyssl):
    return gitlab.Gitlab(url, private_token=api_token, ssl_verify=verifyssl)


@lru_cache(maxsize=None)
def get_project(url, api_token, proj_id, verifyssl) -> Project:
    return get_gitlab(url, api_token, verifyssl).projects.get(proj_id)
