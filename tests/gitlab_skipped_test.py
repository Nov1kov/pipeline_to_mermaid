import unittest

from pipeline_mermaid.generators import GraphGenerator, GanttGenerator, JourneyGenerator
from tests.utils import StubObject


class GitlabSkipped(unittest.TestCase):

    def setUp(self):
        self.jobs = [
            StubObject({'id': '730991283',
                        'allow_failure': False,
                        'status': 'failed',
                        'stage': 'build',
                        'started_at': '2020-09-12T12:26:05.370Z',
                        'finished_at': '2020-09-12T12:26:41.665Z',
                        'name': 'android'}),
            StubObject({'id': '730991284',
                        'status': 'success',
                        'stage': 'build',
                        'started_at': '2020-09-12T12:26:05.370Z',
                        'finished_at': '2020-09-12T12:26:47.665Z',
                        'name': 'ios'}),
            StubObject({'id': '730991285',
                        'status': 'skipped',
                        'stage': 'deploy',
                        'started_at': None,
                        'finished_at': None,
                        'name': 's3'}),
            StubObject({'id': '730991286',
                        'status': 'skipped',
                        'stage': 'deploy',
                        'started_at': None,
                        'finished_at': None,
                        'name': 'firebase'}),
            StubObject({'id': '730991287',
                        'status': 'skipped',
                        'stage': 'deploy',
                        'started_at': None,
                        'finished_at': None,
                        'name': 'play market'}),

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
730991284(ios)
730991285(s3)
730991286(firebase)
730991287(play market)

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

    def test_gantt(self):
        result = GanttGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section build
android :crit, 730991283, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:41.665Z
ios : 730991284, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:47.665Z

section deploy
s3 :done, 730991285, after 730991284, 15s
firebase :done, 730991286, after 730991284, 15s
play market :done, 730991287, after 730991284, 15s
```''', result)

    def test_journey(self):
        result = JourneyGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
journey
section build
  android: 1
  ios: 5
section deploy
  s3: -1: skipped
  firebase: -1: skipped
  play market: -1: skipped
```''', result)


if __name__ == '__main__':
    unittest.main()