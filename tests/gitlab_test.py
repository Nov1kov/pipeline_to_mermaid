import unittest

from pipeline_mermaid.gitlab_helper import get_mermaid_generator
from pipeline_mermaid.generators import *


class GitlabHelper(unittest.TestCase):

    def test_get_generator(self):
        for type in ['graph', 'gantt', 'journey', 'another']:
            with self.subTest(type=type):
                if type == 'another':
                    self.assertRaises(Exception, get_mermaid_generator, [], type)
                    continue
                generator = get_mermaid_generator([], type)
                if type == 'graph':
                    self.assertIsInstance(generator, GraphGenerator)
                elif type == 'gantt':
                    self.assertIsInstance(generator, GanttGenerator)
                elif type == 'journey':
                    self.assertIsInstance(generator, JourneyGenerator)


if __name__ == '__main__':
    unittest.main()
