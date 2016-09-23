from __future__ import absolute_import, division, print_function

from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace
from oct.util.playbook import playbook_path

if not show_stack_trace:
    __unittest = True


class CommonAnsibleOptionsTestCase(PlaybookRunnerTestCase):
    def test_verbosity(self):
        self.run_test(
            TestCaseParameters(
                args=['bootstrap', 'host', '-v'],
                expected_calls=[{
                    'playbook_source': playbook_path('bootstrap/host'),
                    'playbook_variables': None,
                    'ansible_options': {
                        'verbosity': 1
                    }
                }]
            )
        )

    def test_extra_verbosity(self):
        self.run_test(
            TestCaseParameters(
                args=['bootstrap', 'host', '-vvvvvv'],
                expected_calls=[{
                    'playbook_source': playbook_path('bootstrap/host'),
                    'playbook_variables': None,
                    'ansible_options': {
                        'verbosity': 6
                    }
                }]
            )
        )

    def test_dry_run(self):
        self.run_test(
            TestCaseParameters(
                args=['bootstrap', 'host', '--dry-run'],
                expected_calls=[{
                    'playbook_source': playbook_path('bootstrap/host'),
                    'playbook_variables': None,
                    'ansible_options': {
                        'check': True
                    }
                }]
            )
        )
