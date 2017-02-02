# Copyright (c) 2017 Catalyst IT Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
A `Client` is a high-level abstraction on top of Distil features. It
exposes the server features with an object-oriented interface, which
encourages dot notation and automatic, but lazy, resources
allocation. A `Client` allows you to control everything.

To create a `Client` instance, you supply an url pointing to the
server and a version number::

    from distilclient import client

    dc = client.Client(\'http://distil.example.com:9999/\', version='2')

which will load the appropriate client based on the specified
version. Optionally, you can also supply a config dictionary::

    from distilclient import client

    dc = client.Client(\'http://distil.example.com:9999/\',
                      version='2', session=session)

The arguments passed to this function will be passed to the client
instances as well.

It's recommended to use `Client` instances instead of accessing the
lower level API as it has been designed to ease the interaction with
the server and it gives enough control for the most common cases.

A simple example for accessing an existing queue through a client
instance - based on the API v2 - would look like::

    from distilclient import client

    dc = client.Client(\'http://distil.example.com:9999/\', version='2')
    usages = dc.usages.list()

Through the queue instance will be then possible to access all the
features associated with the queue itself like posting messages,
getting message and deleting messages.

`Client` uses the lower-level API to access the server, which means
anything you can do with this client instance can be done by accessing
the underlying API, although not recommended.
"""
from distilclient import exceptions
from distilclient.v1 import client as cv1
from distilclient.v2 import client as cv2

_CLIENTS = {'1.0': cv1.Client,
            '1': cv1.Client,
            '2.0': cv2.Client,
            '2': cv2.Client}


def Client(version='1', *args, **kwargs):
    try:
        return _CLIENTS[version](*args, **kwargs)
    except KeyError:
        raise exceptions.VersionNotFoundForAPIMethod(version)
