# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from Queue import Empty
from multiprocessing import Process, Queue
from sys import stderr, stdout
from time import sleep
from timeit import default_timer as timer

from ansible.constants import COLOR_ERROR, COLOR_OK, COLOR_SKIP
from ansible.playbook import Playbook
from ansible.playbook.play import Play
from ansible.playbook.task import Task
from ansible.plugins.callback import CallbackBase
from backports.shutil_get_terminal_size import get_terminal_size
from os import environ
from os.path import join
from re import sub

RUNNING_PREFIX = 'RUNNING'
SUCCESS_PREFIX = 'SUCCESS'
FAILURE_PREFIX = 'FAILURE'
IGNORED_PREFIX = 'IGNORED'
ERRORED_PREFIX = 'ERRORED'
SKIPPED_PREFIX = 'SKIPPED'

# poll at 20 Hz
POLL_DURATION = 0.05

# we need a reasonable amount of width but we do not
# want to take up more than the width of a single line
# a line will look like:
# PREFIX | IDENT [DETAILS DETAILS ...] ------ [TIMESTAMP]
OUTPUT_WIDTH = min(get_terminal_size().columns, 150)
prefix_width = 7  # e.g. `SUCCESS`
prefix_separator_width = 3  # e.g. ` | `
name_padding_width = 1  # e.g. ` ` after name
time_padding_width = 2  # `- ` before time
time_width = 11  # e.g. `[00:00.000]`
IDENTIFIER_WIDTH = OUTPUT_WIDTH - \
                   prefix_width - prefix_separator_width - \
                   name_padding_width - \
                   time_padding_width - time_width

# TODO: determine if there is a better way
MOVE_UP_ONE_LINE = b'\033[F'
CLEAR_LINE = b'\033[K'


def display_workload(queue):
    """
    Async worker to display the workloads as fed
    by the queue. Will attempt to fetch new data
    from the queue at 20Hz, but failing that, it
    will re-render and display the last seen data
    to keep the refresh rate at or above 20Hz.

    :param queue: queue to consume data from
    """
    last_workload = []
    last_num_lines = 0
    while True:
        try:
            workload = queue.get(timeout=POLL_DURATION)
        except Empty:
            workload = last_workload

        # navigate to the top to over-write the last output
        for i in range(last_num_lines):
            stdout.write(MOVE_UP_ONE_LINE)
            if i < last_num_lines - len(workload):
                # if there are lines in the old output which
                # we may not overwrite, just clear them
                stdout.write(CLEAR_LINE)

        # re-render and print the new output
        last_num_lines = 0
        for item in workload:
            last_num_lines += item.render()

        last_workload = workload


class CallbackModule(CallbackBase):
    """
    This module allows for CLI-based Ansible invocations
    to have nicely formatted output that cleanly indicates
    to the users what their CLI call is doing and how far
    along it is in the process.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'pretty_progress'

    def __init__(self, *args, **kwargs):
        # a container for the workloads we are tracking
        self._workloads = []

        # set up for the async worker we use to update
        # the screen at a rate more frequent than that
        # which we get callbacks at
        self._queue = Queue()
        self._worker = Process(target=display_workload, args=(self._queue, ))
        # ensure that the worker thread is reaped if
        # the main thread dies by marking the thread
        # as a daemon
        self._worker.daemon = True
        self._worker.start()

        super(CallbackModule, self).__init__(*args, **kwargs)

    def update_last_workload(self, status):
        """
        Update the last workload to complete and send
        the updated list of workloads to the consumer.

        :param status: status to update to
        """
        self._workloads[-1].complete(status)

    def finalize_last_play(self, status):
        """
        Update the last play to be complete and remove
        any trace of the tasks that were displayed for it
        while it was running if it succeeded.

        :param status: status to update to
        """
        last_play_index = -1
        for i, workload in reversed(list(enumerate(self._workloads))):
            if 'PLAY [' in workload.identifier:
                last_play_index = i
                break

        if last_play_index != -1:
            # we are called on play start, as there is no
            # callback hook for play end, so if we are called
            # on the start of the first play, there will be
            # no previous play to update
            if status == SUCCESS_PREFIX:
                # if we succeeded, nobody cares what tasks ran,
                # so we can hide them; otherwise, we want the
                # users to see the failed tasks
                self._workloads = self._workloads[:last_play_index + 1]

            self._workloads[last_play_index].complete(status)

    def finalize_playbook(self, status):
        """
        Update the playbook and last play status to
        reflect the end of execution.

        :param status: status we want to update to
        """
        self.finalize_last_play(status)

        # we only ever run one playbook before we
        # reset the internal state, so we can assume
        # that there is only one playbook in the
        # list of workloads, and that it is the first
        # item in the list
        self._workloads[0].complete(status)

    def v2_playbook_on_start(self, playbook):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new playbook begins.
        We know that we will only ever run one playbook
        at a time, so we take some liberties with this:
         - we don't attempt to update the current
           workload state as we assume it is empty

        :param playbook: playbook that just started
        """
        self._workloads.append(Workload(playbook))

    def v2_playbook_on_play_start(self, play):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new play begins. We
        need to clean up the last play before we add
        the new one to the workloads.

        :param play: play that just started
        """
        self.finalize_last_play(SUCCESS_PREFIX)
        self._workloads.append(Workload(play))

    def v2_playbook_on_task_start(self, task, is_conditional):
        """
        Implementation of the callback endpoint to be
        fired when execution of a new task begins. We
        only keep track of the last running task, so
        if there is already a task displayed for the
        current play we over-write it.

        :param task: task that just started
        :param is_conditional: if the task is conditional
        """
        if 'TASK' in self._workloads[-1].identifier:
            self._workloads[-1] = Workload(task)
        else:
            self._workloads.append(Workload(task))

    def v2_runner_on_ok(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task finishes executing successfully.
        We assume that the last workload is the last task.

        :param result: result of the last task
        """
        self.update_last_workload(SUCCESS_PREFIX)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        """
        Implementation of the callback endpoint to be
        fired when a task fails to execute successfully.
        If we are not ignoring errors, we will not only
        show the task as failed, but also add the error
        information to the output stream.

        :param result: result of the last task
        :param ignore_errors: if we should consider this a failure
        """
        status = IGNORED_PREFIX if ignore_errors else FAILURE_PREFIX
        self.update_last_workload(status)

        if not ignore_errors:
            self._workloads.append(Failure(result))

    def v2_runner_on_unreachable(self, result):
        """
        Implementation of the callback endpoint to be
        fired when a task can't reach it's target host.
        We will show the task as errored and append the
        error information to the output stream.

        :param result: result of the last task
        """
        self.update_last_workload(ERRORED_PREFIX)
        self._workloads.append(Failure(result))

    def v2_runner_on_skipped(self, result):
        """
        Implementation of the callback endpoint to be
        fired when task execution is skipped.

        :param result: result of the last task
        """
        self.update_last_workload(SKIPPED_PREFIX)

    def v2_on_any(self, *args, **kwargs):
        """
        Implementation of the callback endpoint to be
        fired *after* any other callback is fired. We
        know that if a callback happened, it could have
        changed the state of the workloads we track,
        so we send the updated state to the consumer
        thread after any callback. If the callback did
        not change the internal state, the consumer
        will just refresh faster than normal, which is
        not an problem. We also will trigger after the
        `v2_playbook_on_stats` endpoint, after which
        we will not have anyone listening to the other
        end of the queue, but we will also be cleaning
        up and exiting soon anyway, so again it is not
        an issue.

        :param args: arguments [ignored]
        :param kwargs: keyword arguments [ignored]
        """
        self._queue.put(self._workloads)

    def v2_playbook_on_stats(self, stats):
        """
        Implementation of the callback endpoint to be
        fired when a playbook is finished. As we are
        only running one playbook at a time, we can
        again make some assumptions about what to do
        here. Specifically:
          - we can assume the last playbook that ran is
            the first item in our workload queue
          - we can clean up the worker thread as there
            will be no more tasks running after this

        :param stats:
        """
        # there isn't a good API for determining failures,
        # so we need to search for them ourselves
        status = SUCCESS_PREFIX
        # task failures are recorded per host per type of
        # failure, so we need to check that any hosts in
        # these sections have occurrences of the failure
        # recorded
        for host in stats.dark:
            if stats.dark[host] > 0:
                # tasks failed to reach their host
                status = FAILURE_PREFIX
                break

        for host in stats.failures:
            if stats.failures[host] > 0:
                # tasks failed to execute
                status = FAILURE_PREFIX
                break

        self.finalize_playbook(status)
        # we need to manually trigger this queue update
        self._queue.put(self._workloads)

        # wait for consumer to post everything we have
        while not self._queue.empty():
            sleep(POLL_DURATION)

        # we are using the multiprocessing queue, which
        # does not implement join() and task_done(), so
        # we cannot reliably know that the consumer has
        # worked on the last element when we see that the
        # queue is empty on our end. No implementation
        # exists with a peek(), either, so we just have
        # to wait for one timeout iteration here and
        # hope for the best.
        sleep(POLL_DURATION)

        self._worker.terminate()
        self._worker.join()


def format_identifier(workload):
    """
    Determine an identifier for the workload.

    :param workload: workload to identify
    :return: identifier for the workload
    """
    if isinstance(workload, Playbook):
        # unfortunately there is no nice way to self-
        # identify for a playbook, so we must access
        # a protected member. Furthermore, we do not
        # necessarily need the full path to the play-
        # book and we can live with the relative path
        # from the origin-ci-tool root.
        # TODO: do this with os.path?
        return 'PLAYBOOK [{}]'.format('origin-ci-tool{}'.format(sub('^.*origin-ci-tool', '', workload._file_name)))
    elif isinstance(workload, Play):
        return 'PLAY [{}]'.format(workload.get_name())
    elif isinstance(workload, Task):
        return 'TASK [{}]'.format(workload.get_name())
    else:
        return 'UNKNOWN'


def format_status(status):
    """
    Format the status of a workload, with
    colors where appropriate.

    :param status: status prefix
    :return: formatted status
    """
    color = 'normal'
    if status == SUCCESS_PREFIX:
        color = COLOR_OK
    elif status == FAILURE_PREFIX or status == ERRORED_PREFIX:
        color = COLOR_ERROR
    elif status == IGNORED_PREFIX or status == SKIPPED_PREFIX:
        color = COLOR_SKIP

    return colorize(status, color=color)


class Workload(object):
    """
    A wrapper for an Ansible workload like a play,
    playbook, task, etc. that knows how to display
    information about the workload in a pretty way.
    """

    def __init__(self, workload):
        """
        Create a Workload wrapper for an Ansible workload.

        :param workload: a play, playbook, task, etc.
        """
        self.identifier = format_identifier(workload)
        self.status = RUNNING_PREFIX
        self.start_time = timer()

        # to be set when we finish this workload
        self.elapsed_time = None

    def __str__(self):
        return self.format()

    def complete(self, status):
        """
        Mark the workload as having been completed.

        :param status: new status to update to
        """
        self.status = format_status(status)
        self.elapsed_time = self.format_runtime()

    def render(self):
        """
        Render a representation of this workload onto
        the screen using stdout.

        :return: number of lines written
        """
        stdout.write(self.format())
        return 1

    def format(self):
        """
        Format a string containing:
        PREFIX | NAME -------------------- [TIME]

        Where PREFIX is one of the above constants,
        NAME is an identifier for the Ansible play
        or playbook being run, and time is a time-
        stamp with format MM:SS.SSS.

        We will truncate the name so that everything
        fits in the allotted width. If the name is
        not going to fit, we will append an ellipsis.

        :return: formatted self-representation
        """
        if len(self.identifier) > IDENTIFIER_WIDTH:
            self.identifier = '{}...'.format(self.identifier[:IDENTIFIER_WIDTH - 3])

        fill_width = IDENTIFIER_WIDTH - len(self.identifier)

        return '{} | {} -{} [{}]\n'.format(
            self.status,
            self.identifier,
            '-' * fill_width,
            self.format_runtime(),
        )

    def format_runtime(self):
        """
        Format the current running time of this
        Workload as a nice string like MM:SS.SSS.

        :return: formatted time
        """
        if self.elapsed_time:
            return self.elapsed_time
        else:
            return '{:02.0f}:{:06.3f}'.format(*divmod(timer() - self.start_time, 60))


def format_result(result):
    """
    Attempt to extract and format information
    about an Ansible workload result.

    :param result: result to inspect
    :return: message
    """
    full_message = format_failure_message(result)
    full_message += format_item_failures(result)
    full_message += format_terminal_output(result)
    # detect internal module failures
    full_message += format_terminal_output(result, stdout_key='module_stdout', stderr_key='module_stderr')
    # detect internal stacktrace crashes
    full_message += format_internal_exception_output(result)
    full_message += format_parsing_error(result)
    return full_message


def format_failure_message(result):
    """
    Output a formatted version of the failure
    message, if the result contains one.

    :param result: result to inspect
    :return: message
    """
    if 'msg' in result:
        # this is most likely a module failure
        if isinstance(result['msg'], list):
            error_message = '\n'.join(result['msg'])
        else:
            error_message = result['msg']

        return '{}\n'.format(error_message)

    return ''


def format_item_failures(result):
    """
    Output a formatted version of the item
    failures, if the result contains any.

    :param result: result to inspect
    :return: message
    """
    if 'results' in result:
        # this is most likely a failure from with_items
        item_preamble = 'The following error messages came from items:'
        item_messages = []
        for item_result in result['results']:
            # the item could possibly contain any
            # valid result output, as any Ansible
            # workload can be looped over
            item_messages.append(format_result(item_result))

        item_messages = [message for message in item_messages if len(message) > 0]
        if len(item_messages) > 0:
            return '{}\n{}'.format(item_preamble, '\n'.join(item_messages))

    return ''


def format_terminal_output(result, stdout_key='stdout', stderr_key='stderr'):
    """
    Output a formatted version of the terminal
    output (std{out,err}), if the result contains
    either.

    :param stdout_key: where stdout is recorded
    :param stderr_key: where stderr is recorded
    :param result: result to inspect
    :return: formatted output message
    """
    output_message = ''
    if stdout_key in result:
        # this is most likely a shell/command/raw failure
        if len(result[stdout_key]) > 0:
            output_message += '{}\n{}\n'.format('Output to stdout:', result[stdout_key])

    if stderr_key in result:
        if len(result[stderr_key]) > 0:
            output_message += '{}\n{}\n'.format(colorize('Output to stderr:', color=COLOR_ERROR), result[stderr_key])

    if stdout_key in result and len(result[stdout_key]) == 0 and stderr_key in result and len(result[stderr_key]) == 0:
        output_message = colorize('No output was written to stdout or stderr!', color=COLOR_ERROR)

    return output_message


def format_internal_exception_output(result):
    """
    Output a formatted version of any internal
    errors that Ansible runs into when executing,
    if any are present.

    :param result: result to inspect
    :return: formatted output message
    """
    if 'exception' in result:
        return 'An internal exception occurred:\n{}'.format(result['exception'])

    return ''


def format_parsing_error(result):
    """
    Output a formatted version of any parsing
    errors that Ansible runs into when looking
    at a playbook, if any are present.

    :param result: result to inspect
    :return: formatted output message
    """
    if 'reason' in result:
        return 'Parsing the playbook failed:\n{}'.format(result['reason'])

    return ''


class Failure(object):
    """
    Holds information about a failure that happened
    and can render itself onto the screen.
    """

    def __init__(self, result):
        self.identifier = 'FAILURE'
        self.result = result._result
        self.host = result._host

    def __str__(self):
        return self.format()

    def render(self):
        """
        Render a representation of this failure
        onto the terminal screen.

        :return: number of lines written
        """
        full_message = self.format()
        stderr.write(full_message)
        return full_message.count('\n')

    def format(self):
        """
        Format the failure result nicely.

        :return: the formatted error
        """
        full_message = colorize('A task failed on host `{}`!\n'.format(self.host), color=COLOR_ERROR)
        full_message += format_result(self.result)

        if full_message.count('\n') == 1:
            # we have not been able to get any use-able
            # messages from the result, so we should
            # tell the user to look at the logs
            # TODO: better OS-agnostic filesystem code for this
            log_location = join(environ.get('ANSIBLE_LOG_ROOT_PATH', join('tmp', 'ansible', 'log')), '/', '{}'.format(self.host))
            full_message += 'No useful error messages could be extracted, see full output at {}\n'.format(log_location)

        return full_message


# --- begin "pretty"
#
# pretty - A miniature library that provides a Python print and stdout
# wrapper that makes colored terminal text easier to use (e.g. without
# having to mess around with ANSI escape sequences). This code is public
# domain - there is no license except that you must leave this header.
#
# Copyright (C) 2008 Brian Nez <thedude at bri1 dot com>
#
# http://nezzen.net/2008/06/23/colored-text-in-python-using-ansi-escape-sequences/

codeCodes = {
    'black': '0;30',
    'bright gray': '0;37',
    'blue': '0;34',
    'white': '1;37',
    'green': '0;32',
    'bright blue': '1;34',
    'cyan': '0;36',
    'bright green': '1;32',
    'red': '0;31',
    'bright cyan': '1;36',
    'purple': '0;35',
    'bright red': '1;31',
    'yellow': '0;33',
    'bright purple': '1;35',
    'dark gray': '1;30',
    'bright yellow': '1;33',
    'magenta': '0;35',
    'bright magenta': '1;35',
    'normal': '0',
}


def colorize(text, color):
    """String in color."""
    return u"\033[%sm%s\033[0m" % (codeCodes[color], text)


# --- end "pretty"
