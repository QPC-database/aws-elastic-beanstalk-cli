# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import re

import six
from six import print_
from six.moves import input
import logging

from ebcli.core import globals

LOG = logging.getLogger(__name__)


def echo_and_justify(justify, *args):
    print_(*_convert_to_strings(args, justify=justify))


def echo(*args):
    print_(*_convert_to_strings(args), sep=' ')


def _convert_to_strings(list_of_things, justify=0):
    scalar_types = six.string_types + six.integer_types
    for data in list_of_things:
        if isinstance(data, unicode):
            yield data.encode('utf8').ljust(justify)
        elif isinstance(data, scalar_types) or hasattr(data, '__str__'):
            yield str(data).ljust(justify)
        else:
            LOG.error('echo called with an unsupported data type')


def log_info(message):
    globals.app.log.info(message)


def log_warning(message):
    globals.app.log.warn(message)


def log_error(message):
    globals.app.log.error(message)


def get_input(output, default=None):
    # importing readline module allows user to use bash commands
    ## such as Ctrl+A etc.
    import readline

    # Trim spaces
    result = input(output + ': ').strip()
    if not result:
        result = default
    return result


def prompt(output, default=None):
    return get_input('(' + output + ')', default)


def prompt_for_unique_name(default, unique_list):
    assert default not in unique_list, 'Default name is not unique'

    while True:
        result = prompt('default is "' + default + '"', default=default)
        if result in unique_list:
            echo('Sorry that name already exists, try another.')
        else:
            break

    return result


def prompt_for_environment_name(default_name='myEnv',
                                prompt_text='Enter Environment Name'):
    """ Validate env_name: Spec says:
     Constraint: Must be from 4 to 23 characters in length.
       The name can contain only letters, numbers, and hyphens.
      It cannot start or end with a hyphen.
    """
    constraint_pattern = '^[a-z0-9][a-z0-9-]{2,21}[a-z0-9]$'
    #  Edit default name to fit standards.

    if not re.match(constraint_pattern, default_name):
        if not re.match('^[a-z0-9].*', default_name):  # begins correctly
            default_name = 'eb-' + default_name
        default_name = default_name.replace('_', '-')
        default_name = re.sub('[^a-z0-9A-Z-]', '', default_name)
        if len(default_name) > 23:
            default_name = default_name[:22]
        if not re.match('.*[a-z0-9]$', default_name):  # end correctly
            default_name += '0'

    while True:
        echo(prompt_text)
        env_name = prompt('default is ' + default_name)
        if not env_name:
            return default_name
        if re.match(constraint_pattern, env_name.lower()):
            break
        else:
            echo('Environment name must be 4 to 23 characters in length. It '
                 'can only contain letters, numbers, and hyphens. It can not '
                 'start or end with a hyphen')

    return env_name


def prompt_for_cname(default=None):
    # Validate cname: spec says:
    # Constraint: Must be from 4 to 23 characters in length.
    # The name can contain only letters, numbers, and hyphens.
    # It cannot start or end with a hyphen.
    while True:
        echo('Enter DNS CNAME prefix')
        if default:
            cname = prompt('default is ' + default)
        else:
            cname = prompt('defaults to an auto-generated value')
        if not cname:
            return default
        if re.match('^[a-z0-9][a-z0-9-]{2,61}[a-z0-9]$', cname.lower()):
            break
        else:
            echo('CNAME must be 4 to 63 characters in length. It can'
                 ' only contain letters, numbers, and hyphens. It can not '
                 'start or end with a hyphen')

    return cname