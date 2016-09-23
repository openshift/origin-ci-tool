# coding=utf-8
from __future__ import absolute_import, division, print_function

from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace
from oct.util.playbook import playbook_path

if not show_stack_trace:
    __unittest = True


class PrepareRepositoriesTestCase(PlaybookRunnerTestCase):
    def test_prepare_repositories(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'repositories'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/repositories'),
                'playbook_variables': None
            }]
        ))
