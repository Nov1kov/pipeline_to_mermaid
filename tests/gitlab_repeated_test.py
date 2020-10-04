import unittest

from pipeline_mermaid.generators import *

from tests.utils import StubObject


class GitlabRepeated(unittest.TestCase):

    def setUp(self):
        self.jobs = [
            StubObject({'id': '730991283',
                        'status': 'success',
                        'stage': 'build',
                        'started_at': '2020-09-12T12:26:05.370Z',
                        'finished_at': '2020-09-12T12:26:41.665Z',
                        'name': 'android'}),
            StubObject({'id': '730991285',
                        'status': 'success',
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
            StubObject({'id': '730994567',
                        'status': 'success',
                        'stage': 'notify',
                        'started_at': '2020-09-12T12:32:43.757Z',
                        'finished_at': '2020-09-12T12:33:35.406Z',
                        'name': 'slack'}),
        ]

    def test_graph_lr(self):
        result = GraphGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;
classDef running fill:white,stroke:#1f75cb,color:black;

730991283(android)
730991285(s3)
730991286(firebase)
730991287(slack)
730994567(slack)

730991283 --> 730991285
730991283 --> 730991286
730991285 --> 730994567
730991286 --> 730994567

class 730991283 success
class 730991285 success
class 730991286 success
class 730991287 failed
class 730994567 success
```''', result)


if __name__ == '__main__':
    unittest.main()
