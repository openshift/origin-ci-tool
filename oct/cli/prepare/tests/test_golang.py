# coding=utf-8
from __future__ import absolute_import, division, print_function

from oct.cli.prepare.golang import golang_version_for_preset
from oct.cli.util.preset_option import Preset
from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace

if not show_stack_trace:
    __unittest = True


class PrepareGolangTestCase(PlaybookRunnerTestCase):
    def test_default(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang'],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {}
            }],
        ))

    def test_preset(self):
        preset = Preset.origin_master
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--for', preset],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {
                    'origin_ci_golang_version': golang_version_for_preset(preset)
                }
            }],
        ))

    def test_version(self):
        version = '1.6.3'
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--version', version],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {
                    'origin_ci_golang_version': version
                }
            }],
        ))

    def test_repo(self):
        repo = 'reponame'
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repo', repo],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {
                    'origin_ci_golang_disabledrepos': '*',
                    'origin_ci_golang_enabledrepos': repo
                }
            }],
        ))

    def test_repos(self):
        repos = ['reponame', 'otherrepo']
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repo', repos[0], '--repo', repos[1]],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {
                    'origin_ci_golang_disabledrepos': '*',
                    'origin_ci_golang_enabledrepos': ','.join(repos)
                }
            }],
        ))

    def test_repourl(self):
        repourl = 'https://www.myrepo.com/whatever'
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repourl', repourl],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {
                    'origin_ci_golang_tmp_repourls': [repourl]
                }
            }],
        ))

    def test_tmp_repourls(self):
        repourls = ['https://www.myrepo.com/whatever', 'https://www.myrepo.com/ok']
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repourl', repourls[0], '--repourl', repourls[1]],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {
                    'origin_ci_golang_tmp_repourls': repourls
                }
            }],
        ))

    def test_repo_and_repourl(self):
        repo = 'reponame'
        repourl = 'https://www.myrepo.com/whatever'
        self.run_test(TestCaseParameters(
            args=['prepare', 'golang', '--repo', repo, '--repourl', repourl],
            expected_calls=[{
                'playbook_relative_path': 'prepare/golang',
                'playbook_variables': {
                    'origin_ci_golang_disabledrepos': '*',
                    'origin_ci_golang_enabledrepos': repo,
                    'origin_ci_golang_tmp_repourls': [repourl]
                }
            }],
        ))
