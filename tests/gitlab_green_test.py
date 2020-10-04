import unittest

from pipeline_mermaid.generators import GraphGenerator, GanttGenerator, JourneyGenerator
from tests.utils import StubObject


class GitlabGreen(unittest.TestCase):

    def setUp(self):
        self.jobs = [
            StubObject({'id': '730991283',
                        'status': 'success',
                        'stage': 'test',
                        'started_at': '2020-09-12T12:26:05.370Z',
                        'finished_at': '2020-09-12T12:26:41.665Z',
                        'name': 'unit tests'}),
            StubObject({'id': '730991284',
                        'status': 'success',
                        'stage': 'build',
                        'started_at': '2020-09-12T12:26:42.182Z',
                        'finished_at': '2020-09-12T12:27:38.126Z',
                        'name': 'build'}),
            StubObject({'id': '730991285',
                        'status': 'success',
                        'stage': 'deploy',
                        'started_at': '2020-09-12T12:27:43.757Z',
                        'finished_at': '2020-09-12T12:28:35.406Z',
                        'name': 's3'}),
            StubObject({'id': '730991286',
                        'status': 'success',
                        'stage': 'deploy',
                        'started_at': '2020-09-12T12:27:43.757Z',
                        'finished_at': '2020-09-12T12:28:44.406Z',
                        'name': 'firebase'}),
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

    def test_gantt(self):
        result = GanttGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section test
unit tests : 730991283, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:41.665Z

section build
build : 730991284, 2020-09-12T12:26:42.182Z, 2020-09-12T12:27:38.126Z

section deploy
s3 : 730991285, 2020-09-12T12:27:43.757Z, 2020-09-12T12:28:35.406Z
firebase : 730991286, 2020-09-12T12:27:43.757Z, 2020-09-12T12:28:44.406Z
```''', result)

    def test_journey(self):
        result = JourneyGenerator(self.jobs).to_mermaid()
        self.assertEqual('''```mermaid
journey
section test
  unit tests: 5
section build
  build: 5
section deploy
  s3: 5
  firebase: 5
```''', result)


if __name__ == '__main__':
    unittest.main()