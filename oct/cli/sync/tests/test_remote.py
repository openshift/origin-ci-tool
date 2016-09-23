from __future__ import absolute_import, division, print_function

from oct.cli.util.repository_options import Repository
from oct.tests.unit.playbook_runner_test_case import CLICK_RC_USAGE, PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace
from oct.util.playbook import playbook_path
from os.path import abspath, dirname

if not show_stack_trace:
    __unittest = True


class SyncRemoteTestCase(PlaybookRunnerTestCase):
    def test_no_repo(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote'],
            expected_result=CLICK_RC_USAGE,
            expected_output='Missing argument "repository"'
        ))

    def test_repository(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'origin',
                    'origin_ci_sync_version': 'master'
                }
            }]
        ))

    def test_bad_repository(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.enterprise],
            expected_result=CLICK_RC_USAGE,
            expected_output='using remote servers is not supported'
        ))

    def test_remote(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--remote', 'myupstream'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'myupstream',
                    'origin_ci_sync_version': 'master'
                }
            }]
        ))

    def test_new_remote(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--new-remote', 'myupstream', 'https://mygitserver.com/origin.git'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'myupstream',
                    'origin_ci_sync_address': 'https://mygitserver.com/origin.git',
                    'origin_ci_sync_version': 'master'
                }
            }]
        ))

    def test_remotes(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--remote', 'first', '--new-remote', 'second', 'git.com/origin.git'],
            expected_result=CLICK_RC_USAGE,
            expected_output='new remote and existing remote cannot be specified at once'
        ))

    def test_explicit_destination(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--dest', '/some/remote/path'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'origin',
                    'origin_ci_sync_destination': '/some/remote/path',
                    'origin_ci_sync_version': 'master'
                }
            }]
        ))

    def test_commit(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--commit', 'SHA'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'origin',
                    'origin_ci_sync_version': 'SHA'
                }
            }]
        ))

    def test_branch(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--branch', 'myfeature'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'origin',
                    'origin_ci_sync_version': 'myfeature'
                }
            }]
        ))

    def test_tag(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--tag', 'v1.0.0'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'origin',
                    'origin_ci_sync_version': 'v1.0.0'
                }
            }]
        ))

    def test_refspec_branch(self):
        self.run_test(TestCaseParameters(
            args=['sync', 'remote', Repository.origin, '--refspec', '/pulls/1/head', '--branch', 'myfeature'],
            expected_calls=[{
                'playbook_source': playbook_path('sync/remote'),
                'playbook_variables': {
                    'origin_ci_sync_repository': Repository.origin,
                    'origin_ci_sync_remote': 'origin',
                    'origin_ci_sync_version': 'myfeature',
                    'origin_ci_sync_refspec': '/pulls/1/head:myfeature'
                }
            }]
        ))