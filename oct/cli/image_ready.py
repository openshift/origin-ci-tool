# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, pass_context, ClickException, option, UsageError

from .util.click import quiet_echo

from .util.boto3 import value_for_tag, image_info

from .util.cloud_provider.image_options import operating_system_option, stage_option, ami_id_option
from .util.cloud_provider.common_options import Provider, provider_option

import boto3
from datetime import datetime

_SHORT_HELP = 'Check if the specified or most recent matching image is tagged ready.'


@command(
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

Examine the cloud provider images matching the specified criteria to
see if the most recently created - or user-specified - image has been
tagged ready, indicating that it has passed acceptance testing.

\b
Examples:
  See if the latest RHEL "base" image (A.K.A. AMI) in AWS has passed acceptance tests
  $ oct image_ready --provider aws --operating_system rhel --stage base

  Check if the latest centos "build" image is *not* ready in AWS, suppress non-error output (e.g. for use in a script):
  $ oct image_ready --provider aws --operating_system centos --stage build --needs-validation --quiet
''',
)
@operating_system_option
@provider_option
@stage_option
@ami_id_option
@pass_context
@option('--needs-validation', '-n', is_flag=True, help='Returns true (0) if the newest matching image is not tagged ready.')
@option('--quiet', '--silent', '-q', 'quiet', is_flag=True, help='Suppress standard output')
def image_ready(context, operating_system, provider, stage, ami_id, needs_validation, quiet):
    if ami_id:
        if provider != Provider.aws:
            raise UsageError("AMI ID only makes sense with cloud provider AWS")
        if operating_system or stage:
            raise UsageError("AMI ID can't be used with search criteria like --operating-system or --stage")
    if provider == Provider.aws:
        _aws_image_ready(operating_system, stage, ami_id, needs_validation, quiet)


def _aws_image_ready(operating_system, stage, ami_id, needs_validation, quiet):
    """
    Fail (exit non-zero) if no matching image is found

    If we are asking if the newest matching image is *non-ready*
    (i.e. `--needs_validation`), succeed (exit 0) if one or more
    matching images are found and the *newest* one is not tagged
    *ready*

    Otherwise, return succeed (exit 0) if one or more matching
    images are found and the *newest* one is tagged *ready*

    :param operating_system: operating system tag to match on AMI
    :param stage:  image build stage to match on AMI
    :param ami_id: unique ID specifying AWS AMI; can't be used with
                   operating_system and stage options
    :param needs_validation: when True, check if the newest matching
                   AMI is not yet tagged ready. When False, check
                   instead if it has been tagged ready
    """
    filter = []
    if operating_system:
        filter.append({'Name': 'tag:operating_system', 'Values': [operating_system]})
    if stage:
        filter.append({'Name': 'tag:image_stage', 'Values': [stage]})
    client = boto3.client('ec2')
    res = None
    if ami_id:
        res = client.describe_images(ImageIds=[ami_id])
    else:
        res = client.describe_images(Filters=filter)
    # Sort the matching images from newest to oldest:
    images = sorted(res['Images'], key=lambda (x): datetime.strptime(x['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=True)
    if not res['Images']:
        raise ClickException(message="No image was found matching the provided tags")
    newest = images[0]
    ready = value_for_tag(newest['Tags'], 'ready').lower() == 'yes'
    message = "{} created {} is".format(image_info(newest), newest['CreationDate'])
    # handle behavior for needs_validation
    if ready:
        message += " ready"
        if needs_validation:
            raise ClickException(message=message)
        else:
            quiet_echo(quiet, message)
    else:
        message += " not ready"
        if needs_validation:
            quiet_echo(quiet, message)
        else:
            raise ClickException(message=message)
