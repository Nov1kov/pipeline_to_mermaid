import os

from pipeline_mermaid.generators import GanttGenerator
from pipeline_mermaid.gitlab_utils import get_project


# https://github.community/t/feature-request-support-mermaid-markdown-graph-diagrams-in-md-files/1922/27
class GitlabHelper:

    def __init__(self, debug=False):
        self.debug = debug
        self.proj_id = os.environ['CI_PROJECT_ID']
        self.gitlab_host = 'https://' + os.environ['CI_SERVER_HOST']

    def get_project(self):
        return get_project(self.gitlab_host, os.environ['GITLAB_API_TOKEN'], self.proj_id, True)

    def show_pipeline_to_merge_request(self):
        project = self.get_project()
        merge_request = self.__get_mr_by_branch(os.environ['CI_COMMIT_BRANCH'])
        if merge_request:
            pipeline = project.pipelines.get(id=os.environ['CI_PIPELINE_ID'])
            jobs = pipeline.jobs.list()
            text = GanttGenerator(jobs).to_mermaid()
            merge_request.notes.create({"body": text})

    def __get_mr_by_branch(self, branch_name):
        mr_list = self.get_project().mergerequests.list(source_branch=branch_name)
        if mr_list:
            return mr_list[0]

    def test_pipeline(self, pipeline_id):
        project = self.get_project()
        #merge_request = project.mergerequests.get(id=os.environ['CI_MERGE_REQUEST_IID'])
        pipeline = project.pipelines.get(pipeline_id)
        jobs = pipeline.jobs.list()
        print(jobs)


if __name__ == "__main__":
    gl = GitlabHelper()
    gl.show_pipeline_to_merge_request()