# coding=utf-8
from __future__ import absolute_import, division, print_function

from oct.cli.version import __version__
from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace

if not show_stack_trace:
    __unittest = True


class VersionTestCase(PlaybookRunnerTestCase):
    def test_version(self):
        self.run_test(TestCaseParameters(
            args=['version'],
            expected_output=__version__
        ))
