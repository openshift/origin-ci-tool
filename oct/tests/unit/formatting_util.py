# coding=utf-8
from difflib import ndiff

from yaml import dump


def format_assertion_failure(message, expectation=None, extra=None):
    """
    Format an assertion failure message nicely.

    :param message: base failure message
    :param expectation: expectation statement
    :param extra: extra details
    :return:
    """
    failure = [message]
    if expectation:
        failure.append(format_expectation(expectation[0], expectation[1], diff=True))

    if extra:
        failure.append(extra)
    return '\n'.join(failure)


def format_expectation(actual, expected, diff=False):
    """
    Format a expected/got tuple nicely.

    :param expected: object
    :param actual: object
    :param diff: whether or not to also display the diff
    :return: formatted text
    """
    actual_data = dump(data=actual, default_flow_style=False, explicit_start=True)
    expected_data = dump(data=expected, default_flow_style=False, explicit_start=True)
    expectation = 'Actual:\n{}\nExpected:\n{}'.format(
        actual_data,
        expected_data
    )
    if diff:
        expectation += '\nDiff:\n{}'.format(
            ''.join(ndiff(actual_data.splitlines(1), expected_data.splitlines(1)))
        )

    return expectation
