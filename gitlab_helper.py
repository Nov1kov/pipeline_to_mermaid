import os

from gitlab_utils import get_project, pipeline_to_mermaid


# https://github.community/t/feature-request-support-mermaid-markdown-graph-diagrams-in-md-files/1922/27
class GitlabHelper:

    def __init__(self, debug=False):
        self.debug = debug
        self.proj_id = os.environ['CI_PROJECT_ID']
        self.gitlab_host = 'https://' + os.environ['CI_SERVER_HOST']

    def get_project(self):
        return get_project(self.gitlab_host, os.environ['GITLAB_API_TOKEN'], self.proj_id, True)

    def show_pipeline_to_merge_request(self, pipeline_id):
        project = self.get_project()
        #merge_request = project.mergerequests.get(id=os.environ['CI_MERGE_REQUEST_IID'])
        pipeline = project.pipelines.get(pipeline_id)
        jobs = pipeline.jobs.list()
        text = pipeline_to_mermaid(jobs)
        print(jobs)



if __name__ == "__main__":
    gl = GitlabHelper()
    gl.show_pipeline_to_merge_request('189128481')