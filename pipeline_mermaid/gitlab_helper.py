import os
import sys

from pipeline_mermaid.generators import GanttGenerator, GraphGenerator, JourneyGenerator
from pipeline_mermaid.gitlab_utils import get_project


# https://github.community/t/feature-request-support-mermaid-markdown-graph-diagrams-in-md-files/1922/27
class GitlabHelper:

    def __init__(self, debug=False):
        self.debug = debug
        self.proj_id = os.environ['CI_PROJECT_ID']
        if 'CI_SERVER_URL' in os.environ:
            self.gitlab_host = os.environ['CI_SERVER_URL']
        else:
            self.gitlab_host = 'https://' + os.environ['CI_SERVER_HOST']

    def get_project(self):
        return get_project(self.gitlab_host, os.environ['GITLAB_API_TOKEN'], self.proj_id, True)

    def show_pipeline(self, pipeline_id=0, type='gantt', merge_request_id=0, message=''):
        if not merge_request_id:
            merge_request = self.__get_mr()
        else:
            merge_request = self.get_project().mergerequests.get(merge_request_id)
        if not pipeline_id:
            pipeline_id = os.environ['CI_PIPELINE_ID']
        self.__show_pipeline_in_mr(merge_request, pipeline_id, type, message)

    def __show_pipeline_in_mr(self, merge_request, pipeline_id, type, message):
        if not merge_request:
            return
        text = ''
        if message:
            text += message
        text += '\n' + self.pipeline_as_mermaid(pipeline_id, type)
        merge_request.notes.create({"body": text})

    def __get_mr(self):
        if 'CI_MERGE_REQUEST_IID' in os.environ:
            return self.get_project().mergerequests.get(os.environ['CI_MERGE_REQUEST_IID'])
        elif 'CI_COMMIT_BRANCH' in os.environ:
            return self.__get_mr_by_branch(os.environ['CI_COMMIT_BRANCH'])
        return self.__get_mr_by_branch(os.environ['CI_COMMIT_REF_NAME'])

    def __get_mr_by_branch(self, branch_name):
        mr_list = self.get_project().mergerequests.list(source_branch=branch_name)
        if mr_list:
            return mr_list[0]

    def pipeline_as_mermaid(self, pipeline_id, type):
        project = self.get_project()
        pipeline = project.pipelines.get(id=pipeline_id)
        jobs = pipeline.jobs.list()
        generator = get_mermaid_generator(jobs, type)
        return generator.to_mermaid()


def get_mermaid_generator(jobs, type):
    if type == 'gantt':
        return GanttGenerator(jobs)
    elif type == 'graph':
        return GraphGenerator(jobs)
    elif type == 'journey':
        return JourneyGenerator(jobs)
    else:
        raise Exception("Unknown type of diagram")


if __name__ == "__main__":
    gl = GitlabHelper()
    result = eval("GitlabHelper." + sys.argv[1])(gl, *sys.argv[2:])
