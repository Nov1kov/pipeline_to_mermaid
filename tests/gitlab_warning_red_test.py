import unittest

from pipeline_mermaid.generators import GraphGenerator, GanttGenerator, JourneyGenerator
from tests.utils import StubObject


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

730991283 --> 730991285
730991283 --> 730991286
730991285 --> 730991287
730991286 --> 730991287

class 730991283 success
class 730991285 warning
class 730991286 success
class 730991287 failed
```''', result)

    def test_gantt(self):
        result = GanttGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section build
android : 730991283, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:41.665Z

section deploy
s3 :crit, active, 730991285, 2020-09-12T12:26:42.182Z, 2020-09-12T12:27:38.126Z
firebase : 730991286, 2020-09-12T12:26:42.346Z, 2020-09-12T12:27:41.991Z

section notify
slack :crit, 730991287, 2020-09-12T12:27:43.757Z, 2020-09-12T12:28:35.406Z
```''', result)

    def test_journey(self):
        result = JourneyGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
journey
section build
  android: 5
section deploy
  s3: 3
  firebase: 5
section notify
  slack: 1
```''', result)


if __name__ == '__main__':
    unittest.main()