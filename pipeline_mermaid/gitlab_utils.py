from datetime import datetime
from functools import lru_cache

import gitlab
from gitlab.v4.objects import Project

GITLAB_FORMAT_DATETIME = '%Y-%m-%dT%H:%M:%S.%fZ'

@lru_cache(maxsize=None)
def get_gitlab(url, api_token, verifyssl):
    return gitlab.Gitlab(url, private_token=api_token, ssl_verify=verifyssl)


@lru_cache(maxsize=None)
def get_project(url, api_token, proj_id, verifyssl) -> Project:
    return get_gitlab(url, api_token, verifyssl).projects.get(proj_id)


def str_to_datetime(str_dt):
    return datetime.strptime(str_dt, GITLAB_FORMAT_DATETIME)


def datetime_to_srt(datetime):
    return datetime.datetime.strftime(datetime.datetime.now(), GITLAB_FORMAT_DATETIME)