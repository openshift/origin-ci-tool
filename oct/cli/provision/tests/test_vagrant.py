from __future__ import absolute_import, division, print_function

from oct.cli.provision.vagrant import OperatingSystem, Provider, Stage
from oct.config import CONFIG
from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace, CLICK_RC_USAGE
from oct.util.playbook import playbook_path

if not show_stack_trace:
    __unittest = True


class ProvisionVagrantTestCase(PlaybookRunnerTestCase):
    def test_default(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant'],
            expected_calls=[{
                'playbook_source': playbook_path('provision/vagrant-up'),
                'playbook_variables': {
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                    'origin_ci_vagrant_os': OperatingSystem.fedora,
                    'origin_ci_vagrant_provider': Provider.libvirt,
                    'origin_ci_vagrant_stage': Stage.install,
                    'origin_ci_vagrant_ip': '10.245.2.2',
                    'origin_ci_vagrant_hostname': 'openshiftdevel'
                }
            }]
        ))

    def test_os(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant', '--os', 'centos'],
            expected_calls=[{
                'playbook_source': playbook_path('provision/vagrant-up'),
                'playbook_variables': {
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                    'origin_ci_vagrant_os': OperatingSystem.centos,
                    'origin_ci_vagrant_provider': Provider.libvirt,
                    'origin_ci_vagrant_stage': Stage.install,
                    'origin_ci_vagrant_ip': '10.245.2.2',
                    'origin_ci_vagrant_hostname': 'openshiftdevel'
                }
            }]
        ))

    def test_provider(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant', '--provider', 'virtualbox'],
            expected_calls=[{
                'playbook_source': playbook_path('provision/vagrant-up'),
                'playbook_variables': {
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                    'origin_ci_vagrant_os': OperatingSystem.fedora,
                    'origin_ci_vagrant_provider': Provider.virtualbox,
                    'origin_ci_vagrant_stage': Stage.install,
                    'origin_ci_vagrant_ip': '10.245.2.2',
                    'origin_ci_vagrant_hostname': 'openshiftdevel'
                }
            }]
        ))

    def test_stage(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant', '--stage', 'base'],
            expected_calls=[{
                'playbook_source': playbook_path('provision/vagrant-up'),
                'playbook_variables': {
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                    'origin_ci_vagrant_os': OperatingSystem.fedora,
                    'origin_ci_vagrant_provider': Provider.libvirt,
                    'origin_ci_vagrant_stage': Stage.base,
                    'origin_ci_vagrant_ip': '10.245.2.2',
                    'origin_ci_vagrant_hostname': 'openshiftdevel'
                }
            }]
        ))

    def test_ip(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant', '--master-ip', '127.0.0.1'],
            expected_calls=[{
                'playbook_source': playbook_path('provision/vagrant-up'),
                'playbook_variables': {
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                    'origin_ci_vagrant_os': OperatingSystem.fedora,
                    'origin_ci_vagrant_provider': Provider.libvirt,
                    'origin_ci_vagrant_stage': Stage.install,
                    'origin_ci_vagrant_ip': '127.0.0.1',
                    'origin_ci_vagrant_hostname': 'openshiftdevel'
                }
            }]
        ))

    def test_custom(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant', '--os', 'centos', '--stage', 'bare', '--provider', 'vmware_fusion'],
            expected_calls=[{
                'playbook_source': playbook_path('provision/vagrant-up'),
                'playbook_variables': {
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                    'origin_ci_vagrant_os': OperatingSystem.centos,
                    'origin_ci_vagrant_provider': Provider.vmware,
                    'origin_ci_vagrant_stage': Stage.bare,
                    'origin_ci_vagrant_ip': '10.245.2.2',
                    'origin_ci_vagrant_hostname': 'openshiftdevel'
                }
            }, {
                'playbook_source': playbook_path('provision/vagrant-docker-storage'),
                'playbook_variables': {
                    'origin_ci_vagrant_provider': Provider.vmware,
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                    'origin_ci_vagrant_hostname': 'openshiftdevel'
                }
            }]
        ))

    def test_vmware_nonbare(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant', '--provider', 'vmware_fusion'],
            expected_result=CLICK_RC_USAGE,
            expected_output='Only the bare stage is supported for the vmware_fusion provider.'
        ))

    def test_destroy(self):
        self.run_test(TestCaseParameters(
            args=['provision', 'vagrant', '--destroy'],
            expected_calls=[{
                'playbook_source': playbook_path('provision/vagrant-down'),
                'playbook_variables': {
                    'origin_ci_vagrant_home_dir': CONFIG['vagrant_home']
                }
            }]
        ))