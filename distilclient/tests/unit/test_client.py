# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ddt
import mock

from distilclient import client
from distilclient import exceptions
from distilclient.tests.unit import utils
import distilclient.v1.client
import distilclient.v2.client


@ddt.ddt
class ClientTest(utils.TestCase):

    @mock.patch("distilclient.v1.client.Client")
    def test_init_client_with_string_v1_version(self, mock_client):
        mock_client('1', 'foo', auth_url='quuz')
        mock_client.assert_called_once_with('1', 'foo', auth_url='quuz')

    @mock.patch.object(distilclient.v2.client, 'Client')
    def test_init_client_with_string_v2_version(self, mock_client):
        mock_client('2', 'foo', auth_url='quuz')
        mock_client.assert_called_once_with('2', 'foo', auth_url='quuz')

    @ddt.data(None, '', '3', 'v1', 'v2', 'v1.0', 'v2.0')
    def test_init_client_with_unsupported_version(self, v):
        self.assertRaises(exceptions.VersionNotFoundForAPIMethod,
                          client.Client, v)
