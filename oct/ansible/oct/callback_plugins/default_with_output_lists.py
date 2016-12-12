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

        if 'stdout' in result:
            result['stdout_lines'] = result['stdout'].splitlines()
            del result['stdout']

        if 'stderr' in result:
            result['stderr_lines'] = result['stderr'].splitlines()
            del result['stderr']

        if 'module_stdout' in result:
            result['module_stdout_lines'] = result['module_stdout'].splitlines()
            del result['module_stdout']

        if 'module_stderr' in result:
            result['module_stderr_lines'] = result['module_stderr'].splitlines()
            del result['module_stderr']

        return super(CallbackModule, self)._dump_results(result=result, indent=4)
