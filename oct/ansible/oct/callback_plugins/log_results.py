# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import contextmanager
from functools import wraps
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


@contextmanager
def bind_logger(**kwargs):
    global logger
    logger = logger.bind(**kwargs)
    try:
        yield
    finally:
        logger = logger.unbind(*kwargs.keys())


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

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error(callback=func.__name__, args=args, kwargs=kwargs, exc_info=True)

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

    @wraps(func)
    def wrapper(self, playbook):
        return func(self, playbook)

    return wrapper


def log_callback_name(func):
    """ Add the function name to the log. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with bind_logger(callback=func.__name__):
            func(*args, **kwargs)

    return wrapper


def log_callback_id(func):
    """ Add identification information about the event to the log. """

    @wraps(func)
    def wrapper(callback_module, workload, *args, **kwargs):
        name = workload.get_name()
        uuid = str(workload._uuid)
        location = '{}:{}'.format(*determine_location_for_workload(workload))
        with bind_logger(name=name, uuid=uuid, location=location):
            func(callback_module, workload, *args, **kwargs)

    return wrapper


def determine_location_for_workload(workload):
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


def log_callback_result(func):
    """ Add the `host` and `result` callback parameters to the log. """

    @wraps(func)
    def wrapper(callback_module, raw_result, *args, **kwargs):
        host = raw_result._host.get_name()
        sanitize_results(raw_result._result)
        with bind_logger(host=host, result=raw_result._result):
            func(callback_module, raw_result, *args, **kwargs)

    return wrapper


def sanitize_results(data):
    """
    Sanitize the results to remove unnecessary fields.
    Removes Ansible internal fields that the user doesn't need in their output
    files and `stdout_lines` if `stdout` is present -- we can let people load
    the data and format it however they want, but we don't want to store it
    twice.
    """
    remove_ansible_data(data)
    if 'results' in data:
        for result in data['results']:
            remove_ansible_data(result)
            if 'stdout' in result and 'stdout_lines' in result:
                del result['stdout_lines']


def remove_ansible_data(result):
    """ Remove internal fields that should not be logged. """
    for key in result.keys():
        if key.startswith('_ansible'):
            del result[key]


class CallbackModule(CallbackBase):
    """ Log playbook, play, and task execution to a file formatted as json. """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'log_results'
    CALLBACK_NEEDS_WHITELIST = True

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
    @log_callback_name
    def v2_playbook_on_start(self, playbook):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new playbook begins.

        :param playbook: playbook which began execution
        """
        logger.info(playbook=playbook._file_name)

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_playbook_on_import_for_host(self, result, imported_file):
        """
        Implementation of the callback endpoint to be
        fired when an import occurs on a host.

        :param result: result of the import action
        :param imported_file: which file was imported by the host
        """
        logger.info(imported_file=imported_file)

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        """
        Implementation of the callback endpoint to be
        fired when an import fails on a host.

        :param result: result of the import action
        :param missing_file: which file was not found on the host
        """
        logger.error(missing_file=missing_file)

    @log_exceptions
    @log_callback_name
    def v2_playbook_on_include(self, included_file):
        """
        Implementation of the callback endpoint to be
        fired when an include statement is executed.

        :param included_file: which file was imported by the host
        """
        logger.info(included_file=included_file)

    @log_exceptions
    @log_callback_name
    def v2_playbook_on_no_hosts_matched(self):
        """
        Implementation of the callback endpoint to be
        fired when a playbook finds no hosts to execute on.
        """
        logger.info()

    @log_exceptions
    @log_callback_name
    def v2_playbook_on_no_hosts_remaining(self):
        """
        Implementation of the callback endpoint to be
        fired when a playbook has no hosts remaining
        to execute on.
        """
        logger.info()

    @log_exceptions
    @log_callback_name
    def v2_playbook_on_setup(self):
        """
        Implementation of the callback endpoint to be
        fired when a setup task is executed.
        """
        logger.info()

    @log_exceptions
    @log_callback_id
    @log_callback_name
    def v2_playbook_on_play_start(self, play):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new play begins.

        :param play: play which began execution
        """
        logger.info()

    @log_exceptions
    @log_callback_id
    @log_callback_name
    def v2_playbook_on_task_start(self, task, is_conditional):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new task begins.

        :param task:task which began execution
        :param is_conditional: whether or not this task is conditional
        """
        logger.info(is_conditional=is_conditional)

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_failed(self, result, ignore_errors=False):
        """
        Implementation of the callback endpoint to be
        fired when a task fails to execute successfully.

        :param result: result of the task execution
        :param ignore_errors: if we should consider this a failure
        """
        logger.error(ignore_errors=ignore_errors)

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_ok(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task executes successfully.

        :param result: result of the task execution
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_skipped(self, result):
        """
        Implementation of the callback endpoint to be
        fired when task execution is skipped.

        :param result: result of the task execution
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_unreachable(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task fails to reach a target host.

        :param result: result of the task execution
        """
        logger.error()

    @log_exceptions
    @log_callback_id
    @log_callback_name
    def v2_runner_on_no_hosts(self, task):
        """
        Implementation of the callback endpoint to be
        fired when a task finds no hosts to execute on.

        :param task: task which did not execute
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_async_ok(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task asynchronously executes
        successfully.

        :param result: result of the task execution
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_async_failed(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task fails to execute asynchronously
        successfully.

        :param result: result of the task execution
        """
        logger.error()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_async_poll(self, result):
        """
        Implementation of the callback endpoint to be
        fired when an async task is polled.

        :param result: result of the poll
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_item_on_ok(self, result):
        """
        Implementation of the callback endpoint to be
        fired when an item on a task finishes successfully.

        :param result: result of the item execution
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_item_on_failed(self, result):
        """
        Implementation of the callback endpoint to be
        fired when an item on a task fails.

        :param result: result of the item execution
        """
        logger.error()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_item_on_skipped(self, result):
        """
        Implementation of the callback endpoint to be
        fired when an item on a task is skipped.

        :param result: result of the item execution
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_retry(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task is retried.

        :param result: result of the item execution
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_runner_on_file_diff(self, result, diff):
        """
        Implementation of the callback endpoint to be
        fired when a file diff is displayed.

        :param result: result of the item execution
        """
        logger.info()

    @log_exceptions
    @log_callback_result
    @log_callback_name
    def v2_playbook_on_notify(self, result, handler):
        """
        Implementation of the callback endpoint to be
        fired when a task is "changed" and has notifiers.

        :param result: result of the item execution
        :param handler: name of the handler
        """
        logger.info(handler=handler)

    @log_exceptions
    @log_callback_id
    @log_callback_name
    def v2_playbook_on_cleanup_task_start(self, task):
        """
        Implementation of the callback endpoint to be
        fired when a cleanup task is executed.

        :param task: cleanup task
        """
        logger.info()

    @log_exceptions
    @log_callback_id
    @log_callback_name
    def v2_playbook_on_handler_task_start(self, task):
        """
        Implementation of the callback endpoint to be
        fired when a handler is executed.

        :param task: handler task
        """
        logger.info()

    @log_exceptions
    @log_callback_name
    def v2_playbook_on_vars_prompt(
            self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None
    ):
        """
        Implementation of the callback endpoint to be
        fired when a prompt is displayed.
        """
        logger.info(varname=varname)

    @log_callback_name
    @log_callback_result
    @log_exceptions
    def v2_on_file_diff(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a file diff is displayed.

        :param result: result of the item execution
        """
        logger.info()

    @log_exceptions
    @log_callback_name
    def v2_playbook_on_stats(self, stats):
        """
        Implementation of the callback endpoint to be
        fired when playbook stats are displayed.

        :param result: result of the item execution
        """
        logger.info()
