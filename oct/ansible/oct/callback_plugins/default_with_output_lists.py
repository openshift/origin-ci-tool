# coding=utf-8
"""
A callback module that limits the amount of overlong lines.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy
from datetime import datetime

from ansible.plugins.callback.default import CallbackModule as DefaultCallbackModule


class CallbackModule(DefaultCallbackModule):
    """
    This CallbackModule overrides the default stdout
    callback plugin to always use arrays for stderr
    and stdout, whether from commands or from modules,
    and to always output indented JSON no matter the
    verbosity level. This module also adds the current
    system time into a `generated_timestamp` field.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'default_with_output_lists'

    def _dump_results(self, original_result, indent=None, sort_keys=True, keep_invocation=False):
        """
        Dump results from a module.

        :param original_result: results from the module
        :param indent: how many spaces to use for indentation
        :param sort_keys: whether or not to sort keys
        :param keep_invocation: whether or not to keep the module invocation
        :return: module results
        :rtype: str
        """
        result = deepcopy(original_result)
        result['generated_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        for entry in ['stdout', 'stderr', 'module_stdout', 'module_stderr', 'results']:
            split_entry = '{}_lines'.format(entry)

            if entry in result and callable(getattr(result[entry], 'splitlines', None)):
                result[entry] = result[entry].splitlines()
            elif split_entry in result:
                result[entry] = result[split_entry]

            if split_entry in result:
                del result[split_entry]

        return super(CallbackModule, self)._dump_results(result=result, indent=4)
