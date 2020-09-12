import os
import unittest
from unittest import mock

from gitlab_utils import pipeline_to_mermaid


class GitlabMermaid(unittest.TestCase):

    def setUp(self):
        pass

    def test_graph_green_pipeline(self):
        jobs = [
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
        result = pipeline_to_mermaid(jobs)
        self.assertEqual('''```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef classWarn fill:white,stroke:#fc9403,color:black;
classDef canceled fill:white,stroke:#999,color:black;

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

    def test_graph_red_pipeline(self):
        jobs = [
            StubObject({'id': '730991283',
                        'status': 'success',
                        'stage': 'build',
                        'name': 'android'}),
            StubObject({'id': '730991285',
                        'status': 'success',
                        'stage': 'deploy',
                        'name': 's3'}),
            StubObject({'id': '730991286',
                        'status': 'success',
                        'stage': 'deploy',
                        'name': 'firebase'}),
            StubObject({'id': '730991287',
                        'status': 'failed',
                        'stage': 'notify',
                        'name': 'slack'}),

        ]
        result = pipeline_to_mermaid(jobs)
        self.assertEqual('''```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef classWarn fill:white,stroke:#fc9403,color:black;
classDef canceled fill:white,stroke:#999,color:black;

730991283(android)
730991285(s3)
730991286(firebase)
730991287(slack)

730991283 --> 730991285
730991283 --> 730991286
730991285 --> 730991287
730991286 --> 730991287

class 730991283 success
class 730991285 success
class 730991286 success
class 730991287 failed
```''', result)


class StubObject:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [StubObject(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, StubObject(b) if isinstance(b, dict) else b)


if __name__ == '__main__':
    unittest.main()