# coding=utf-8
from __future__ import absolute_import, division, print_function

from oct.cli.util.repository_options import Repository
from oct.tests.unit.playbook_runner_test_case import CLICK_RC_USAGE, PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace
from oct.util.playbook import playbook_path
from os.path import abspath, dirname

if not show_stack_trace:
    __unittest = True


class SyncLocalTestCase(PlaybookRunnerTestCase):
    def test_no_repo(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'local'],
            expected_result=CLICK_RC_USAGE,
            expected_output='Missing argument "repository"'
        ))

    def test_repository(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'local', Repository.origin],
            expected_calls=[{
                'playbook_source': playbook_path('sync/local'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_version': 'master'
                }
            }]
        ))

    def test_explicit_source(self):
        # we need to use a real path on the host since Click validates the local path
        self.run_test(TestCaseParameters(
            args=['sync', 'local', Repository.origin, '--src', abspath(dirname(__file__))],
            expected_calls=[{
                'playbook_source': playbook_path('sync/local'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_source': abspath(dirname(__file__)),
                    'origin_ci_sync_version': 'master'
                }
            }]
        ))

    def test_explicit_destination(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'local', Repository.origin, '--dest', '/some/remote/path'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/local'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_destination': '/some/remote/path',
                    'origin_ci_sync_version': 'master'
                }
            }]
        ))

    def test_commit(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'local', Repository.origin, '--commit', 'SHA'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/local'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_version': 'SHA'
                }
            }]
        ))

    def test_branch(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'local', Repository.origin, '--branch', 'myfeature'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/local'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_version': 'myfeature'
                }
            }]
        ))

    def test_tag(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'local', Repository.origin, '--tag', 'v1.0.0'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/local'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_version': 'v1.0.0'
                }
            }]
        ))

    def test_refspec_branch(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'local', Repository.origin, '--refspec', '/pulls/1/head', '--branch', 'myfeature'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/local'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_version': 'myfeature',
                    'origin_ci_sync_refspec': '/pulls/1/head:myfeature'
                }
            }]
        ))
