import unittest

from pipeline_mermaid.generators import GraphGenerator, GanttGenerator, JourneyGenerator
from tests.utils import StubObject


class GitlabRunning(unittest.TestCase):

    def setUp(self):
        self.jobs = [
            StubObject({'id': '730991283',
                        'status': 'running',
                        'stage': 'build',
                        'started_at': '2020-09-12T12:26:05.370Z',
                        'created_at': '2020-09-12T21:45:02.379Z',
                        'finished_at': None,
                        'name': 'android'}),
            StubObject({'id': '730991284',
                        'status': 'running',
                        'stage': 'build',
                        'started_at': '2020-09-12T12:26:05.370Z',
                        'created_at': '2020-09-12T21:45:02.379Z',
                        'finished_at': None,
                        'name': 'ios'}),
            StubObject({'id': '730991285',
                        'status': 'created',
                        'stage': 'deploy',
                        'started_at': None,
                        'finished_at': None,
                        'created_at': '2020-09-12T21:45:02.379Z',
                        'name': 'slack:android'}),
            StubObject({'id': '730991286',
                        'status': 'created',
                        'stage': 'deploy',
                        'started_at': None,
                        'finished_at': None,
                        'created_at': '2020-09-12T21:45:02.379Z',
                        'name': 'slack:ios'}),
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
730991285(slack:android)
730991286(slack:ios)

730991283 --> 730991285
730991284 --> 730991285
730991283 --> 730991286
730991284 --> 730991286

class 730991283 running
class 730991284 running
class 730991285 skipped
class 730991286 skipped
```''', result)

    def test_gantt(self):
        result = GanttGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section build
android :active, 730991283, 2020-09-12T21:45:02.379Z, 15s
ios :active, 730991284, 2020-09-12T21:45:02.379Z, 15s

section deploy
slack-android :done, 730991285, after 730991283, 15s
slack-ios :done, 730991286, after 730991283, 15s
```''', result)

    def test_journey(self):
        result = JourneyGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
journey
section build
  android: -1: running
  ios: -1: running
section deploy
  slack-android: -1: created
  slack-ios: -1: created
```''', result)


if __name__ == '__main__':
    unittest.main()