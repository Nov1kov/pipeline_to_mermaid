from itertools import groupby

from gitlab_utils import str_to_datetime, datetime_to_srt


class GraphGenerator:

    def __init__(self, jobs):
        self.jobs = jobs

    def to_mermaid(self):
        self.jobs.sort(key=lambda k: k.id)
        scheme = 'graph LR\n'
        scheme += self.__styles()
        scheme += self.__job_names()
        scheme += self.__job_flow_charts()
        scheme += self.__job_statuses()
        return f'```mermaid\n{scheme}```'

    def __styles(self):
        return '''
classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;
classDef running fill:white,stroke:#1f75cb,color:black;
'''

    def __job_names(self):
        text = '\n'
        for job in self.jobs:
            text += f"{job.id}({job.name})\n"
        return text

    def __job_flow_charts(self):
        text = '\n'
        last_stage_groups = []
        for k, g in groupby(self.jobs, key=lambda j: j.stage):
            stage_groups = list(g)
            for job in stage_groups:
                for prev_job in last_stage_groups:
                    text += f'{prev_job.id} --> {job.id}\n'
            last_stage_groups = stage_groups
        return text

    def __job_statuses(self):
        text = '\n'
        for job in self.jobs:
            if job.status == 'failed' and job.allow_failure or job.status == 'pending':
                class_status = 'warning'
            elif job.status == 'created' or job.status == 'manual' or job.status == 'canceled':
                class_status = 'skipped'
            else:
                class_status = job.status
            text += f"class {job.id} {class_status}\n"
        return text


def fix_job_name(name):
    return name.replace(':', '-')


class GanttGenerator:

    def __init__(self, jobs):
        self.jobs = jobs

    def to_mermaid(self):
        self.jobs.sort(key=lambda k: k.id)
        scheme = 'gantt\n'
        scheme += self.__date_format()
        last_job_id = None
        for k, g in groupby(self.jobs, key=lambda j: j.stage):
            stage_jobs = list(g)
            scheme += self.__stage(k, stage_jobs, last_job_id)
            last_job_id = self.__get_finished_stage_at(stage_jobs)
        return f'```mermaid\n{scheme}```'

    def __date_format(self):
        return '''
dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S
'''

    def __stage(self, stage, jobs, last_job_id):
        text = f'\nsection {stage}\n'
        for job in jobs:
            text += f'{fix_job_name(job.name)} :{self.__get_status(job)} {job.id}, ' + self.__get_job_length(job, last_job_id)
        return text

    def __get_status(self, job):
        if job.status == 'failed':
            if job.allow_failure:
                return 'crit, active,'
            return 'crit,'
        if job.status == 'running':
            return 'active,'
        if job.status == 'skipped' or job.status == 'created' or job.status == 'manual' or job.status == 'canceled':
            return 'done,'
        return ''

    def __get_finished_stage_at(self, stage_jobs):
        finished_jobs = [job for job in stage_jobs if job.finished_at]
        if finished_jobs:
            job = max(finished_jobs, key=lambda j: str_to_datetime(j.finished_at))
            return job.id
        if stage_jobs:
            return stage_jobs[0].id
        return None

    def __get_job_length(self, job, last_job_id):
        if not job.started_at or not job.finished_at:
            if last_job_id:
                return f'after {last_job_id}, 15s\n'
            return f'{job.created_at}, 15s\n'
        return f'{job.started_at}, {job.finished_at}\n'
