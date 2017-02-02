# Copyright 2010 Jacob Kaplan-Moss

# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from distilclient.common.apiclient import exceptions as client_exceptions
from distilclient import exceptions
from distilclient.tests.unit import utils
from distilclient.tests.unit.v2 import fakes
from distilclient.v2 import usage

cs = fakes.FakeClient()


class UsageTest(utils.TestCase):

    # Testcases for class Share
    def setUp(self):
        super(UsageTest, self).setUp()
