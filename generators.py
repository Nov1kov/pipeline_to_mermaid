from itertools import groupby


class GraphGenerator():

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
            class_status = 'warning' if job.status == 'failed' and job.allow_failure == True else job.status
            text += f"class {job.id} {class_status}\n"
        return text


class GanttGenerator():

    def __init__(self, jobs):
        self.jobs = jobs

    def to_mermaid(self):
        self.jobs.sort(key=lambda k: k.id)
        scheme = 'gantt\n'
        scheme += self.__date_format()
        for k, g in groupby(self.jobs, key=lambda j: j.stage):
            scheme += self.__stage(k, list(g))
        return f'```mermaid\n{scheme}```'

    def __date_format(self):
        return '''
dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S
'''

    def __stage(self, stage, jobs):
        text = f'\nsection {stage}\n'
        for job in jobs:
            text += f'{job.name} :{self.__get_status(job)} {job.id}, {job.started_at}, {job.finished_at}\n'
        return text

    def __get_status(self, job):
        if job.status == 'failed':
            return 'crit,'
        if job.status == 'running':
            return 'active,'
        if job.status == 'skipped':
            return 'done,'
        return ''