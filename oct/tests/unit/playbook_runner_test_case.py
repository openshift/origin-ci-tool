# coding=utf-8
from unittest import TestCase

from click.testing import CliRunner
from mock import patch
from oct.oct import oct_command
from oct.tests.unit.formatting_util import format_assertion_failure, format_expectation
from oct.util.playbook_runner import PlaybookRunner
from os import environ

# Allow for run-time triggering of stack trace output
show_stack_trace = 'SHOW_STACK_TRACE' in environ
if not show_stack_trace:
    __unittest = show_stack_trace

# Click does not expose these exit codes, so we need to define them
CLICK_RC_OK = 0
CLICK_RC_EXCEPTION = 1
CLICK_RC_USAGE = 2


class TestCaseParameters(object):
    def __init__(self, args, expected_result=CLICK_RC_OK, expected_calls=None, expected_output=None):
        """
        Parameterize a Click PlaybookRunner test case.

        :param args: command-line arguments to Click
        :param expected_result: expected exit code of the command-line invocation
        :param expected_calls: expected calls to PlaybookRunner.run()
        :param expected_output: phrase expected to be in the command line output
        """
        self.args = args
        self.expected_result = expected_result
        self.expected_output = expected_output
        self.expected_calls = expected_calls


class PlaybookRunnerTestCase(TestCase):
    """
    Set up a common test case that validates correct
    interaction with the PlaybookRunner.
    """

    def setUp(self):
        """
        Mock out the `run()` method on the PlaybookRunner
        so that we can validate that it is called correctly.
        """
        self._call_metadata = []
        patcher = patch.object(
            target=PlaybookRunner,
            attribute='run',
            new=lambda playbook_runner, playbook_source, playbook_variables=None: \
                self._call_metadata.append({
                    'playbook_source': playbook_source,
                    'playbook_variables': playbook_variables,
                    'ansible_options': playbook_runner._ansible_options
                })
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_test(self, parameters):
        """
        Run a Click PlaybookRunner test case.

        :param parameters: a TestCaseParameters instance
        """
        result = CliRunner().invoke(cli=oct_command, args=parameters.args)
        self.assertEqual(
            parameters.expected_result,
            result.exit_code,
            format_assertion_failure(
                message='Command did not exit with correct code.',
                expectation=(parameters.expected_result, result.exit_code),
                extra='Full output:\n{}'.format(result.output)
            )
        )
        self.validate_call_metadata(parameters.expected_calls)
        if parameters.expected_output is not None:
            self.assertIn(
                parameters.expected_output,
                result.output,
                msg=format_assertion_failure(
                    message='Phrase `{}` not found in output.'.format(parameters.expected_output),
                    extra='Full output:\n{}'.format(result.output)
                )
            )

    def validate_call_metadata(self, expected_calls):
        """
        Validate that the metadata recorded by our mock
        matches what was expected for the test. If the
        expected data contains an `ansible_options` key,
        we will helpfully only check that the metadata
        we collected previously contains the options that
        the user specified, and ignore any they did not,
        to allow users to specify only the ones that they
        care about.

        :param expected_calls: expected call metadata
        """
        if expected_calls is None:
            expected_calls = []

        self._expected_calls = expected_calls

        for actual, expected in zip(self._call_metadata, expected_calls):
            # don't pollute output if we don't care about it
            if 'ansible_options' not in expected:
                actual['ansible_options'] = '<ignored>'

        self.make_equality_assertion(
            actual=len(self._call_metadata),
            expected=len(expected_calls),
            message='Invalid number of playbook calls.'
        )

        for i, (actual, expected) in enumerate(zip(self._call_metadata, expected_calls)):
            prefix = '[playbook {}]'.format(i)

            self.make_equality_assertion(
                actual=actual['playbook_source'],
                expected=expected['playbook_source'],
                message='{}: Invalid source.'.format(prefix)
            )

            self.make_equality_assertion(
                actual=actual['playbook_variables'],
                expected=expected['playbook_variables'],
                message='{}: Invalid variables.'.format(prefix)
            )

            # we will be comparing a dictionary in `expected`
            # with a named tuple in the metadata, and we only
            # want to check that the expected keys have the
            # right values
            if 'ansible_options' in expected:
                for option in expected['ansible_options']:
                    self.make_equality_assertion(
                        actual=hasattr(actual['ansible_options'], option),
                        expected=True,
                        message='{}: Extraneous Ansible option {}.'.format(prefix, option)
                    )

                    self.make_equality_assertion(
                        actual=getattr(actual['ansible_options'], option),
                        expected=expected['ansible_options'][option],
                        message='{}: Invalid Ansible option {}.'.format(prefix, option)
                    )

    def make_equality_assertion(self, actual, expected, message):
        """
        Make an assertion about equality, with a nice
        error message that is consistent between tests
        and gives full context to what is being tested.

        :param actual: object
        :param expected: object
        :param message: failure message
        """
        self.assertEqual(
            actual,
            expected,
            msg=format_assertion_failure(
                message=message,
                expectation=(actual, expected),
                extra='Full Call Metadata Context:\n{}'.format(
                    format_expectation(
                        self._call_metadata,
                        self._expected_calls
                    )
                )
            )
        )
