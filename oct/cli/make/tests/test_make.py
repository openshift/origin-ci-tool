# coding=utf-8
from __future__ import absolute_import, division, print_function

from oct.cli.util.repository_options import Repository
from oct.tests.unit.playbook_runner_test_case import CLICK_RC_USAGE, PlaybookRunnerTestCase, TestCaseParameters, \
    show_stack_trace

if not show_stack_trace:
    __unittest = True


class MakeTestCase(PlaybookRunnerTestCase):
    def test_no_repository(self):
        self.run_test(TestCaseParameters(
            args=['make'],
            expected_result=CLICK_RC_USAGE,
            expected_output='Missing argument "repository"',
        ))

    def test_bad_repository(self):
        self.run_test(TestCaseParameters(
            args=['make', 'notarepo'],
            expected_result=CLICK_RC_USAGE,
            expected_output='Invalid value for "repository"',
        ))

    def test_no_target(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin],
            expected_result=CLICK_RC_USAGE,
            expected_output='Missing argument "target"',
        ))

    def test_basic(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin, 'target'],
            expected_calls=[{
                'playbook_relative_path': 'make/main',
                'playbook_variables': {
                    'origin_ci_make_repository': Repository.origin,
                    'origin_ci_make_targets': ['target'],
                },
            }],
        ))

    def test_multiple_targets(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin, 'target', 'second_target'],
            expected_calls=[{
                'playbook_relative_path': 'make/main',
                'playbook_variables': {
                    'origin_ci_make_repository': Repository.origin,
                    'origin_ci_make_targets': ['target', 'second_target'],
                },
            }],
        ))

    def test_one_envar(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin, 'target', '--env', 'KEY=VAL'],
            expected_calls=[{
                'playbook_relative_path': 'make/main',
                'playbook_variables': {
                    'origin_ci_make_repository': Repository.origin,
                    'origin_ci_make_targets': ['target'],
                    'origin_ci_make_parameters': {
                        'KEY': 'VAL',
                    },
                },
            }],
        ))

    def test_envar_equals(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin, 'target', '--env', 'KEY=OTHERKEY=VAL'],
            expected_calls=[{
                'playbook_relative_path': 'make/main',
                'playbook_variables': {
                    'origin_ci_make_repository': Repository.origin,
                    'origin_ci_make_targets': ['target'],
                    'origin_ci_make_parameters': {
                        'KEY': 'OTHERKEY=VAL',
                    },
                },
            }],
        ))

    def test_many_envars(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin, 'target', '--env', 'KEY=VAL', '--env', 'KEY2=VAL', '--env', 'KEY3=VAL'],
            expected_calls=[{
                'playbook_relative_path': 'make/main',
                'playbook_variables': {
                    'origin_ci_make_repository': Repository.origin,
                    'origin_ci_make_targets': ['target'],
                    'origin_ci_make_parameters': {
                        'KEY': 'VAL',
                        'KEY2': 'VAL',
                        'KEY3': 'VAL',
                    },
                },
            }],
        ))

    def test_bad_format_envar(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin, 'target', '--env', 'KEYVAL'],
            expected_result=CLICK_RC_USAGE,
            expected_output='Parameter KEYVAL is invalid',
        ))

    def test_explicit_destination(self):
        self.run_test(TestCaseParameters(
            args=['make', Repository.origin, 'target', '--dest', '/some/path'],
            expected_calls=[{
                'playbook_relative_path': 'make/main',
                'playbook_variables': {
                    'origin_ci_make_repository': Repository.origin,
                    'origin_ci_make_targets': ['target'],
                    'origin_ci_make_destination': '/some/path',
                },
            }],
        ))
