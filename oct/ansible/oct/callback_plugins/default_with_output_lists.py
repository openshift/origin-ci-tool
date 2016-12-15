# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy

from ansible.plugins.callback import default


class CallbackModule(default.CallbackModule):
    """
    This CallbackModule overrides the default stdout
    callback plugin to always use arrays for stderr
    and stdout, whether from commands or from modules,
    and to always output indented JSON no matter the
    verbosity level.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'default_with_output_lists'

    def _dump_results(self, original_result, indent=None, sort_keys=True, keep_invocation=False):
        result = deepcopy(original_result)

        for entry in ['stdout', 'stderr', 'module_stdout', 'module_stderr', 'results']:
            split_entry = '{}_lines'.format(entry)

            if entry in result and callable(getattr(result[entry], 'splitlines', None)):
                result[entry] = result[entry].splitlines()
            elif split_entry in result:
                result[entry] = result[split_entry]

            if split_entry in result:
                del (result[split_entry])

        return super(CallbackModule, self)._dump_results(result=result, indent=4)
