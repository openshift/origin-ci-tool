# coding=utf-8
from __future__ import absolute_import, division, print_function

from mock import patch
from oct.tests.unit.playbook_runner_test_case import CLICK_RC_USAGE, PlaybookRunnerTestCase, \
    TestCaseParameters, show_stack_trace, PlaybookRunCallSpecification

if not show_stack_trace:
    __unittest = True


class PackageAMITestCase(PlaybookRunnerTestCase):
    def setUp(self):
        PlaybookRunnerTestCase.setUp(self)

    def test_tag_empty_value(self):
        self.run_test(
            TestCaseParameters(
                args=['package', 'ami', '--tag', 'env', "--stage=next"],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='package/ami',
                        playbook_variables={'origin_ci_aws_additional_tags': {
                            'env': ''
                        }},
                    )
                ],
            )
        )

    def test_tag_missing_key(self):
        missing_key = '=prod'
        self.run_test(
            TestCaseParameters(
                args=['package', 'ami', '--tag', missing_key, "--stage=next"],
                expected_calls=None,
                expected_result=CLICK_RC_USAGE,
                expected_output="Invalid tag: {} - key must have non-zero length".format(missing_key),
            )
        )

    def test_tag_single(self):
        self.run_test(
            TestCaseParameters(
                args=['package', 'ami', '--tag', 'env=prod', "--stage=next"],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='package/ami',
                        playbook_variables={'origin_ci_aws_additional_tags': {
                            'env': 'prod'
                        }},
                    )
                ],
            )
        )

    def test_tag_multiple(self):
        self.run_test(
            TestCaseParameters(
                args=['package', 'ami', '--tag', 'env=prod', '--tag', "qe=ready", "--stage=next"],
                expected_calls=[
                    PlaybookRunCallSpecification(
                        playbook_relative_path='package/ami',
                        playbook_variables={'origin_ci_aws_additional_tags': {
                            'env': 'prod',
                            'qe': 'ready'
                        }},
                    )
                ],
            )
        )

    def test_tag_mark_ready_overwrite(self):
        to_be_overwritten = 'ready=ack'
        self.run_test(
            TestCaseParameters(
                args=['package', 'ami', '--tag', to_be_overwritten, '--mark-ready'],
                expected_calls=None,
                expected_result=CLICK_RC_USAGE,
                expected_output="Invalid tag: {} - will be overwritten by --mark-ready (ready=yes)".format(to_be_overwritten),
            )
        )

    def test_no_options(self):
        self.run_test(
            TestCaseParameters(
                args=['package', 'ami'],
                expected_calls=None,
                expected_result=CLICK_RC_USAGE,
                expected_output="--stage must be specified",
            )
        )
