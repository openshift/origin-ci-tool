# coding=utf-8
from __future__ import absolute_import, division, print_function

from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace, \
    PlaybookRunCallSpecification

if not show_stack_trace:
    __unittest = True


class BootstrapNodeTestCase(PlaybookRunnerTestCase):
    def test_bootstrap_node(self):
        self.run_test(
            TestCaseParameters(
                args=['bootstrap', 'node'],
                expected_calls=[PlaybookRunCallSpecification(
                    playbook_relative_path='bootstrap/node',
                )],
            )
        )
