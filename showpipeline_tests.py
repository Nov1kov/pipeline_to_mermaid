import os
import unittest
from unittest import mock

from gitlab_utils import pipeline_to_mermaid


class GitlabWarningRed(unittest.TestCase):

    def setUp(self):
        self.jobs = [
            StubObject({'id': '730991283',
                        'status': 'success',
                        'stage': 'build',
                        'started_at': '2020-09-12T12:26:05.370Z',
                        'finished_at': '2020-09-12T12:26:41.665Z',
                        'name': 'android'}),
            StubObject({'id': '730991285',
                        'allow_failure': True,
                        'status': 'failed',
                        'stage': 'deploy',
                        'started_at': '2020-09-12T12:26:42.182Z',
                        'finished_at': '2020-09-12T12:27:38.126Z',
                        'name': 's3'}),
            StubObject({'id': '730991286',
                        'status': 'success',
                        'stage': 'deploy',
                        'started_at': '2020-09-12T12:26:42.346Z',
                        'finished_at': '2020-09-12T12:27:41.991Z',
                        'name': 'firebase'}),
            StubObject({'id': '730991287',
                        'allow_failure': False,
                        'status': 'failed',
                        'stage': 'notify',
                        'started_at': '2020-09-12T12:27:43.757Z',
                        'finished_at': '2020-09-12T12:28:35.406Z',
                        'name': 'slack'}),

        ]

    def test_graph_lr(self):
        result = pipeline_to_mermaid(self.jobs)
        self.assertEqual('''```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;

730991283(android)
730991285(s3)
730991286(firebase)
730991287(slack)

730991283 --> 730991285
730991283 --> 730991286
730991285 --> 730991287
730991286 --> 730991287

class 730991283 success
class 730991285 warning
class 730991286 success
class 730991287 failed
```''', result)

    def test_grantt(self):
        pass


class GitlabGreen(unittest.TestCase):

    def setUp(self):
        self.jobs = [
            StubObject({'id': '730991283',
                        'status': 'success',
                        'stage': 'test',
                        'name': 'unit tests'}),
            StubObject({'id': '730991284',
                        'status': 'success',
                        'stage': ' build',
                        'name': 'build'}),
            StubObject({'id': '730991285',
                        'status': 'success',
                        'stage': 'deploy',
                        'name': 's3'}),
            StubObject({'id': '730991286',
                        'status': 'success',
                        'stage': 'deploy',
                        'name': 'firebase'}),
        ]

    def test_graph_lr(self):

        result = pipeline_to_mermaid(self.jobs)
        self.assertEqual('''```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;

730991283(unit tests)
730991284(build)
730991285(s3)
730991286(firebase)

730991283 --> 730991284
730991284 --> 730991285
730991284 --> 730991286

class 730991283 success
class 730991284 success
class 730991285 success
class 730991286 success
```''', result)

    def test_grantt(self):
        pass


class GitlabSkipped(unittest.TestCase):

    def setUp(self):
        self.jobs = [
            StubObject({'id': '730991283',
                        'allow_failure': False,
                        'status': 'failed',
                        'stage': 'build',
                        'name': 'android'}),
            StubObject({'id': '730991284',
                        'status': 'success',
                        'stage': 'build',
                        'name': 'ios'}),
            StubObject({'id': '730991285',
                        'status': 'skipped',
                        'stage': 'deploy',
                        'name': 's3'}),
            StubObject({'id': '730991286',
                        'status': 'skipped',
                        'stage': 'deploy',
                        'name': 'firebase'}),
            StubObject({'id': '730991287',
                        'status': 'skipped',
                        'stage': 'deploy',
                        'name': 'firebase'}),

        ]

    def test_graph_lr(self):
        result = pipeline_to_mermaid(self.jobs)
        self.assertEqual('''```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;

730991283(android)
730991284(ios)
730991285(s3)
730991286(firebase)
730991287(firebase)

730991283 --> 730991285
730991284 --> 730991285
730991283 --> 730991286
730991284 --> 730991286
730991283 --> 730991287
730991284 --> 730991287

class 730991283 failed
class 730991284 success
class 730991285 skipped
class 730991286 skipped
class 730991287 skipped
```''', result)

    def test_grantt(self):
        pass


class StubObject:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [StubObject(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, StubObject(b) if isinstance(b, dict) else b)


if __name__ == '__main__':
    unittest.main()