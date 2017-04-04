# coding=utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from oct.cli.prepare.docker import docker_version_for_preset
from oct.cli.util.preset_option import Preset
from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace, \
    PlaybookRunCallSpecification

if not show_stack_trace:
    __unittest = True


class PrepareDockerTestCase(PlaybookRunnerTestCase):
    def test_default(self):
        self.run_test(
            TestCaseParameters(
                args=['prepare', 'docker'],
                expected_calls=[PlaybookRunCallSpecification(
                    playbook_relative_path='prepare/docker',
                )],
            )
        )

    def test_preset(self):
        self.run_test(
            TestCaseParameters(
                args=['prepare', 'docker', '--for', Preset.origin_master],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='prepare/docker',
                        playbook_variables={'origin_ci_docker_version': docker_version_for_preset(Preset.origin_master), },
                    )
                ],
            )
        )

    def test_version(self):
        self.run_test(
            TestCaseParameters(
                args=['prepare', 'docker', '--version', '1.10.3'],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='prepare/docker',
                        playbook_variables={'origin_ci_docker_version': '1.10.3', },
                    )
                ],
            )
        )

    def test_repo(self):
        self.run_test(
            TestCaseParameters(
                args=['prepare', 'docker', '--repo', 'reponame'],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='prepare/docker',
                        playbook_variables={
                            'origin_ci_docker_disabledrepos': ['*'],
                            'origin_ci_docker_enabledrepos': ['reponame'],
                        },
                    )
                ],
            )
        )

    def test_repos(self):
        self.run_test(
            TestCaseParameters(
                args=['prepare', 'docker', '--repo', 'reponame', '--repo', 'otherrepo'],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='prepare/docker',
                        playbook_variables={
                            'origin_ci_docker_disabledrepos': ['*'],
                            'origin_ci_docker_enabledrepos': ['reponame', 'otherrepo'],
                        },
                    )
                ],
            )
        )

    def test_repourl(self):
        self.run_test(
            TestCaseParameters(
                args=['prepare', 'docker', '--repourl', 'https://www.myrepo.com/whatever'],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='prepare/docker',
                        playbook_variables={'origin_ci_docker_tmp_repourls': ['https://www.myrepo.com/whatever'], },
                    )
                ],
            )
        )

    def test_tmp_repourls(self):
        self.run_test(
            TestCaseParameters(
                args=[
                    'prepare', 'docker', '--repourl', 'https://www.myrepo.com/whatever', '--repourl', 'https://www.myrepo.com/ok'
                ],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='prepare/docker',
                        playbook_variables={
                            'origin_ci_docker_tmp_repourls': ['https://www.myrepo.com/whatever', 'https://www.myrepo.com/ok'],
                        },
                    )
                ],
            )
        )

    def test_repo_and_repourl(self):
        self.run_test(
            TestCaseParameters(
                args=['prepare', 'docker', '--repo', 'reponame', '--repourl', 'https://www.myrepo.com/whatever'],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='prepare/docker',
                        playbook_variables={
                            'origin_ci_docker_disabledrepos': ['*'],
                            'origin_ci_docker_enabledrepos': ['reponame'],
                            'origin_ci_docker_tmp_repourls': ['https://www.myrepo.com/whatever'],
                        },
                    )
                ],
            )
        )


class DockerPresetTestCase(TestCase):
    def test_origin_master(self):
        self.assertEqual(docker_version_for_preset(Preset.origin_master), '1.10.3')

    def test_ose_master(self):
        self.assertEqual(docker_version_for_preset(Preset.ose_master), '1.10.3')

    def test_ose_33(self):
        self.assertEqual(docker_version_for_preset(Preset.ose_33), '1.10.3')

    def test_ose_321(self):
        self.assertEqual(docker_version_for_preset(Preset.ose_321), '1.10.3')

    def test_ose_32(self):
        self.assertEqual(docker_version_for_preset(Preset.ose_32), '1.9.1')
