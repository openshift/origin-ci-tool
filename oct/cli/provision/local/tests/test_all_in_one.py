# coding=utf-8
from __future__ import absolute_import, division, print_function

from mock import patch
from oct.cli.provision.local import all_in_one
from oct.cli.provision.local.all_in_one import OperatingSystem, Provider, Stage
from oct.config import vagrant as vagrant_configuration
from oct.config.configuration import Configuration
from oct.config.vagrant import VagrantVMMetadata
from oct.tests.unit.playbook_runner_test_case import CLICK_RC_USAGE, PlaybookRunnerTestCase, \
    TestCaseParameters, show_stack_trace, PlaybookRunCallSpecification

if not show_stack_trace:
    __unittest = True


class ProvisionVagrantTestCase(PlaybookRunnerTestCase):
    def setUp(self):
        PlaybookRunnerTestCase.setUp(self)
        patches = [
            patch.object(
                target=VagrantVMMetadata,
                attribute='load',
                new=lambda _, __: None,
            ),
            patch.object(
                target=VagrantVMMetadata,
                attribute='write',
                new=lambda _: None,
            ),
            patch.object(
                target=VagrantVMMetadata,
                attribute='remove',
                new=lambda _: None,
            ),
            patch.object(
                target=Configuration,
                attribute='_vagrant_hostname_taken',
                new=lambda _, __: False,
            ),
            patch.object(
                target=all_in_one,
                attribute='register_host',
                new=lambda _, __, ___, ____, _____, ______: None,
            ),
            patch.object(
                target=vagrant_configuration,
                attribute='fetch_ssh_configuration',
                new=lambda _, __: None,
            ),
        ]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_default(self):
        self.run_test(
            TestCaseParameters(
                args=['provision', 'local', 'all-in-one'],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='provision/vagrant-up',
                        playbook_variables={
                            'origin_ci_vagrant_os': OperatingSystem.fedora,
                            'origin_ci_vagrant_provider': Provider.virtualbox,
                            'origin_ci_vagrant_stage': Stage.install,
                            'origin_ci_ssh_config_strategy': 'update',
                        },
                    )
                ],
            )
        )

    def test_os(self):
        os = OperatingSystem.centos
        self.run_test(
            TestCaseParameters(
                args=['provision', 'local', 'all-in-one', '--os', os],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='provision/vagrant-up',
                        playbook_variables={'origin_ci_vagrant_os': os, },
                    )
                ],
            )
        )

    def test_provider(self):
        provider = Provider.virtualbox
        self.run_test(
            TestCaseParameters(
                args=['provision', 'local', 'all-in-one', '--provider', provider],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='provision/vagrant-up',
                        playbook_variables={'origin_ci_vagrant_provider': provider, },
                    )
                ],
            )
        )

    def test_stage(self):
        stage = Stage.base
        self.run_test(
            TestCaseParameters(
                args=['provision', 'local', 'all-in-one', '--stage', stage],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='provision/vagrant-up',
                        playbook_variables={'origin_ci_vagrant_stage': stage, },
                    )
                ],
            )
        )

    def test_ip(self):
        ip = '127.0.0.1'
        self.run_test(
            TestCaseParameters(
                args=['provision', 'local', 'all-in-one', '--master-ip', ip],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='provision/vagrant-up',
                        playbook_variables={'origin_ci_vagrant_ip': ip, },
                    )
                ],
            )
        )

    def test_custom(self):
        os = OperatingSystem.centos
        stage = Stage.bare
        provider = Provider.vmware
        self.run_test(
            TestCaseParameters(
                args=['provision', 'local', 'all-in-one', '--os', os, '--stage', stage, '--provider', provider],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='provision/vagrant-up',
                        playbook_variables={
                            'origin_ci_vagrant_os': os,
                            'origin_ci_vagrant_provider': provider,
                            'origin_ci_vagrant_stage': stage,
                        },
                    ), PlaybookRunCallSpecification(
                        playbook_relative_path='provision/vagrant-docker-storage',
                        playbook_variables={'origin_ci_vagrant_provider': provider, },
                    )
                ],
            )
        )

    def test_vmware_nonbare(self):
        self.run_test(
            TestCaseParameters(
                args=['provision', 'local', 'all-in-one', '--provider', 'vmware_fusion'],
                expected_result=CLICK_RC_USAGE,
                expected_output='Only the bare stage is supported for the vmware_fusion provider.',
            )
        )
