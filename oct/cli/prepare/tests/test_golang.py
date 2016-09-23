# coding=utf-8
from __future__ import absolute_import, division, print_function

from oct.cli.prepare.golang import golang_version_for_preset
from oct.cli.util.preset_option import Preset
from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace
from oct.util.playbook import playbook_path

if not show_stack_trace:
    __unittest = True


class PrepareGolangTestCase(PlaybookRunnerTestCase):
    def test_default(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang',
                }
            }]
        ))

    def test_preset(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--for', Preset.origin_master],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang-' + golang_version_for_preset(Preset.origin_master)
                }
            }]
        ))

    def test_version(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--version', '1.10.3'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang-1.10.3'
                }
            }]
        ))

    def test_repo(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repo', 'reponame'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang',
                    'origin_ci_golang_disabledrepos': '*',
                    'origin_ci_golang_enabledrepos': 'reponame'
                }
            }]
        ))

    def test_repos(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repo', 'reponame', '--repo', 'otherrepo'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang',
                    'origin_ci_golang_disabledrepos': '*',
                    'origin_ci_golang_enabledrepos': 'reponame,otherrepo'
                }
            }]
        ))

    def test_repourl(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repourl', 'https://www.myrepo.com/whatever'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang',
                    'origin_ci_golang_tmp_repourls': ['https://www.myrepo.com/whatever']
                }
            }]
        ))

    def test_tmp_repourls(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repourl', 'https://www.myrepo.com/whatever', '--repourl', 'https://www.myrepo.com/ok'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang',
                    'origin_ci_golang_tmp_repourls': ['https://www.myrepo.com/whatever', 'https://www.myrepo.com/ok']
                }
            }]
        ))

    def test_repo_and_repourl(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repo', 'reponame', '--repourl', 'https://www.myrepo.com/whatever'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/golang'),
                'playbook_variables': {
                    'origin_ci_golang_package': 'golang',
                    'origin_ci_golang_disabledrepos': '*',
                    'origin_ci_golang_enabledrepos': 'reponame',
                    'origin_ci_golang_tmp_repourls': ['https://www.myrepo.com/whatever']
                }
            }]
        ))