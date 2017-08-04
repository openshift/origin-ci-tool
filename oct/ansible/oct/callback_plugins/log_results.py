# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from logging import INFO, FileHandler
from os import environ, makedirs
from os.path import exists, join

from ansible.plugins.callback import CallbackBase
from structlog import configure, get_logger
from structlog.stdlib import BoundLogger, LoggerFactory, add_log_level
from structlog.processors import JSONRenderer, TimeStamper, UnicodeDecoder, format_exc_info
from yaml import dump

configure(
    processors=[
        add_log_level,
        TimeStamper(fmt="iso"),
        format_exc_info,
        UnicodeDecoder(),
        JSONRenderer(),
    ], context_class=dict, logger_factory=LoggerFactory(), wrapper_class=BoundLogger, cache_logger_on_first_use=True
)
logger = get_logger('origin-ci-tool')
logger.setLevel(INFO)


def log_exceptions(func):
    """
    Instead of allowing exceptions from the method
    this decorates, log the exception to disk and
    instead fail silently. I know this is insane.
    We want to:
        a) get the full exception output
        b) not pollute std{out,err}
    Ansible does not allow us these simple things.
    So we work around it in a crazy way.

    :param func: function to decorate
    :return: decorated function
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error(
                callback=func.__name__, args=args, kwargs=kwargs,
                exc_info=True)
    return wrapper


def log_exceptions_v2_playbook_on_start(func):
    """
    The Ansible TaskQueueManager inspects the
    declared argument names, but only for the
    `v2_playbook_on_start` method, and if the
    method does not explicitly list `playbook`
    as an argument, it mangles the call. This
    wrapper, therefore, exposes `playbook` as
    an argument.

    :param func: wrapped v2_playbook_on_start
    :return: better wrapper
    """

    def wrapper(self, playbook):
        return func(self, playbook)

    return wrapper


class CallbackModule(CallbackBase):
    """
    Logs results from tasks, per playbook, per host.
    Logfiles are aggregates of YAML snippets that
    describe actions, their results, and where full
    log messages can be found. Full log messages are
    aggregates of YAML snippets that were given to
    the callback, like the result, whether errors are
    to be ignored, etc.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'log_results'
    CALLBACK_NEEDS_WHITELIST = True

    def write_log(self, message, data=None):
        """
        Write a message to the log.

        :param message: message for the log
        :param data: extra data for the log
        """
        if data:
            # sanitize the data to remove Ansible
            # internal fields that the user doesn't
            # need in their output files
            for key in data.keys():
                if key.startswith('_ansible'):
                    del data[key]

            # remove `stdout_lines` if `stdout` is
            # present -- we can let people load the
            # data and format it however they want,
            # but we don't want to store it twice
            if 'results' in data:
                for result in data['results']:
                    if 'stdout' in result and 'stdout_lines' in result:
                        del result['stdout_lines']
        logger.info(message, data=data)

    def log_task_result(self, status, result):
        """
        Log the result of a task.

        :param status: exit status of the task
        :param result: result data from the task
        """
        host = result._host.get_name()
        message = 'Task finished with status "{}" on host "{}"'.format(status, host)
        data = result._result
        self.write_log(message, data)

    def log_message_for_task(self, task, message_prefix):
        """
        Log a message for a task. The message will
        be prepended to a generic stanza identifying
        the task.

        :param task: task to log for
        :param message_prefix: message prefix to write
        """
        task_file, task_line = self.determine_location_for_workload(task)
        self.write_log(
            '{} task "{}" with UUID "task_{}" from "{}:{}".'.format(
                message_prefix,
                task.get_name(),
                task._uuid,
                task_file,
                task_line,
            )
        )

    def determine_location_for_workload(self, workload):
        """
        Determine the file location and line number where
        the Ansible workload is defined. Not every workload
        has a consistent set of entries in `_attributes`, so
        we need to take a more dynamic approach to find one
        that we can (ab)use for this information.

        :param workload: Ansible workload to inspect
        :return: file path, line number
        """
        if not hasattr(workload, '_attributes'):
            return 'unknown', 'unknown'

        for attribute in workload._attributes.values():
            if hasattr(attribute, '_data_source'):
                return attribute._data_source, attribute._line_number

        return 'unknown', 'unknown'

    def __init__(self):
        """ Make sure the log directory exists. """
        super(CallbackModule, self).__init__()
        log_directory = environ.get('ANSIBLE_LOG_ROOT_PATH')
        if not exists(log_directory):
            makedirs(log_directory)
        handler = FileHandler(join(log_directory, 'log.txt'), 'a')
        logger.addHandler(handler)

    @log_exceptions_v2_playbook_on_start
    @log_exceptions
    def v2_playbook_on_start(self, playbook):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new playbook begins.

        :param playbook: playbook which began execution
        """
        self.write_log('Starting execution for playbook at {}'.format(playbook._file_name))

    @log_exceptions
    def v2_playbook_on_import_for_host(self, result, imported_file):
        """
        Implementation of the callback endpoint to be
        fired when an import occurs on a host.

        :param result: result of the import action
        :param imported_file: which file was imported by the host
        """
        # TODO: determine what this result looks like and place it in the right log dir
        host = result._host.get_name()
        self.write_log('Imported file at "{}" on host "{}"'.format(imported_file, host))
        self.write_log(dump(result, default_flow_style=False, explicit_start=True))

    @log_exceptions
    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        """
        Implementation of the callback endpoint to be
        fired when an import fails on a host.

        :param result: result of the import action
        :param missing_file: which file was not found on the host
        """
        # TODO: determine what this result looks like and place it in the right log dir
        host = result._host.get_name()
        self.write_log('Failed to import file at "{}" on host "{}"'.format(missing_file, host))
        self.write_log(dump(result, default_flow_style=False, explicit_start=True))

    @log_exceptions
    def v2_playbook_on_include(self, included_file):
        """
        Implementation of the callback endpoint to be
        fired when an include statement is executed.

        :param included_file: which file was imported by the host
        """
        self.write_log('Included file at "{}"'.format(included_file))

    @log_exceptions
    def v2_playbook_on_setup(self):
        """
        Implementation of the callback endpoint to be
        fired when a setup task is executed. We want
        to handle this case separately from the generic
        task case as setup "tasks" do not contain much
        of the metadata we expect to see on all tasks.
        """
        self.write_log('Running setup for playbook.')

    @log_exceptions
    def v2_playbook_on_play_start(self, play):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new play begins.

        :param play: play which began execution
        """
        play_file, play_line = self.determine_location_for_workload(play)
        self.write_log(
            'Starting execution for play "{}" with name "play_{}" from "{}:{}".'.format(
                play.get_name(),
                play._uuid,
                play_file,
                play_line,
            )
        )

    @log_exceptions
    def v2_playbook_on_task_start(self, task, is_conditional):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new task begins.

        :param task:task which began execution
        :param is_conditional: whether or not this task is conditional
        """
        self.log_message_for_task(task, 'Starting')

    @log_exceptions
    def v2_runner_on_failed(self, result, ignore_errors=False):
        """
        Implementation of the callback endpoint to be
        fired when a task fails to execute successfully.

        :param result: result of the task execution
        :param ignore_errors: if we should consider this a failure
        """
        self.log_task_result('failed', result)

    @log_exceptions
    def v2_runner_on_ok(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task executes successfully.

        :param result: result of the task execution
        """
        self.log_task_result('ok', result)

    @log_exceptions
    def v2_runner_on_skipped(self, result):
        """
        Implementation of the callback endpoint to be
        fired when task execution is skipped.

        :param result: result of the task execution
        """
        self.log_task_result('skipped', result)

    @log_exceptions
    def v2_runner_on_unreachable(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task fails to reach a target host.

        :param result: result of the task execution
        """
        self.log_task_result('unreachable', result)

    @log_exceptions
    def v2_runner_on_no_hosts(self, task):
        """
        Implementation of the callback endpoint to be
        fired when a task finds no hosts to execute on.

        :param task: task which did not execute
        """
        self.log_message_for_task(task, 'No hosts found for')

    @log_exceptions
    def v2_runner_on_async_ok(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task asynchronously executes
        successfully.

        :param result: result of the task execution
        """
        self.log_task_result('async ok', result)

    @log_exceptions
    def v2_runner_on_async_failed(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task fails to execute asynchronously
        successfully.

        :param result: result of the task execution
        """
        self.log_task_result('async failed', result)

    @log_exceptions
    def v2_playbook_on_no_hosts_matched(self):
        """
        Implementation of the callback endpoint to be
        fired when a playbook finds no hosts to execute on.
        """
        self.write_log('No hosts matched.')

    @log_exceptions
    def v2_playbook_on_no_hosts_remaining(self):
        """
        Implementation of the callback endpoint to be
        fired when a playbook has no hosts remaining
        to execute on.
        """
        self.write_log('No hosts remaining.')

        # TODO: unimplemented methods follow - do we need them?
        # def v2_runner_item_on_ok(self, result):
        # def v2_runner_item_on_failed(self, result):
        # def v2_runner_item_on_skipped(self, result):
        # def v2_runner_retry(self, result):
        # def v2_runner_on_file_diff(self, result, diff):
        # def v2_playbook_on_notify(self, result, handler):
        # def v2_playbook_on_cleanup_task_start(self, task):
        # def v2_playbook_on_handler_task_start(self, task):
        # def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None,
        #                                confirm=False, salt_size=None, salt=None, default=None):
        # def v2_on_file_diff(self, result):
        # def v2_playbook_on_stats(self, stats):


def callback_generic_event(func):
    def wrapper(*args, **kwargs):
        logger.bind(callback=func.__name__)
        func(*args, **kwargs)
        logger.unbind('callback')

    return wrapper


def callback_result_event(func):
    def wrapper(callback_module, raw_result, *args, **kwargs):
        host = raw_result._host.get_name()
        result = santitize_result(raw_result._result)
        ansible_workload_reference = {
            'uuid': raw_result._task._uuid,
            'type': 'task'
        }
        logger.bind(host=host, result=result, ansible_workload_reference=ansible_workload_reference)
        callback_generic_event(func)(callback_module, raw_result, *args, **kwargs)
        logger.unbind('host', 'result', 'ansible_workload_reference')

    return wrapper


def callback_start_event(func):
    def wrapper(callback_module, ansible_workload, *args, **kwargs):
        ansible_workload_reference = {
            'uuid': ansible_workload._uuid,
            'type': type(ansible_workload).__name__.lower()
        }
        logger.bind(ansible_workload_reference=ansible_workload_reference)
        callback_generic_event(func)(callback_module, ansible_workload, *args, **kwargs)
        logger.unbind('ansible_workload_reference')

    return wrapper
