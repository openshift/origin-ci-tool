from __future__ import absolute_import, division, print_function

from oct.cli.prepare.docker import docker_version_for_preset
from oct.cli.prepare.golang import golang_version_for_preset
from oct.cli.util.preset_option import Preset
from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace
from oct.util.playbook import playbook_path

if not show_stack_trace:
    __unittest = True


class PrepareAllTestCase(PlaybookRunnerTestCase):
    def test_default(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'all'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/main'),
                'playbook_variables': {
                    'origin_ci_docker_package': 'docker-' + docker_version_for_preset(Preset.origin_master),
                    'origin_ci_golang_package': 'golang-' + golang_version_for_preset(Preset.origin_master),
                }
            }]
        ))

    def test_preset(self):
        self.run_test(TestCaseParameters(
            args=['prepare', 'all', '--for', 'ose/master'],
            expected_calls=[{
                'playbook_source': playbook_path('prepare/main'),
                'playbook_variables': {
                    'origin_ci_docker_package': 'docker-' + docker_version_for_preset(Preset.ose_master),
                    'origin_ci_golang_package': 'golang-' + golang_version_for_preset(Preset.ose_master),
                }
            }]
        ))
