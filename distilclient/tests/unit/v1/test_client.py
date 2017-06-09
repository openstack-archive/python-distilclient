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

import mock

from distilclient.tests.unit import utils
from distilclient.v1 import client as v1_client


class FakeResponse(object):
    status_code = 200
    result = {}

    def __init__(self, status_code, result):
        self.status_code = status_code
        self.result = result

    def json(self):
        return self.result


class ClientTest(utils.TestCase):

    def setUp(self):
        super(ClientTest, self).setUp()
        self.tenant = 'fake_tenant'
        self.start = "2017-01-01"
        self.end = "2017-02-01"
        self.distil_url = "http://127.0.0.1:9999/v2"

    @mock.patch("keystoneauth1.identity.generic.Password.get_token")
    @mock.patch("requests.post")
    def test_collect_usage(self, mock_post, mock_get_token):
        mock_get_token.return_value = 'fake_token'
        mock_post.return_value = FakeResponse(200, {})
        client = v1_client.HTTPClient(distil_url=self.distil_url)
        client.collect_usage()
        expect_url = 'http://127.0.0.1:9999/collect_usage'
        expect_headers = {'X-Auth-Token': 'fake_token',
                          'Content-Type': 'application/json'}
        mock_post.assert_called_once_with(expect_url,
                                          headers=expect_headers,
                                          verify=True)

    @mock.patch("keystoneauth1.identity.generic.Password.get_token")
    @mock.patch("requests.get")
    def test_last_collected(self, mock_get, mock_get_token):
        mock_get_token.return_value = 'fake_token'
        mock_get.return_value = FakeResponse(200, {})
        client = v1_client.HTTPClient(distil_url=self.distil_url)
        client.last_collected()
        expect_url = 'http://127.0.0.1:9999/last_collected'
        expect_headers = {'X-Auth-Token': 'fake_token',
                          'Content-Type': 'application/json'}
        mock_get.assert_called_once_with(expect_url,
                                         headers=expect_headers,
                                         verify=True)

    @mock.patch("keystoneauth1.identity.generic.Password.get_token")
    @mock.patch("requests.get")
    def test_get_rated(self, mock_get, mock_get_token):
        mock_get_token.return_value = 'fake_token'
        mock_get.return_value = FakeResponse(200, {})
        client = v1_client.HTTPClient(distil_url=self.distil_url)
        client.get_rated(self.tenant, self.start, self.end)
        mock_get.assert_called_once_with('http://127.0.0.1:9999/get_rated',
                                         headers={'X-Auth-Token':
                                                  'fake_token'},
                                         params={'tenant': 'fake_tenant',
                                                 'end': '2017-02-01',
                                                 'start': '2017-01-01'},
                                         verify=True)

    @mock.patch("keystoneauth1.identity.generic.Password.get_token")
    @mock.patch("requests.get")
    def test_get_usage(self, mock_get, mock_get_token):
        mock_get_token.return_value = 'fake_token'
        mock_get.return_value = FakeResponse(200, {})
        client = v1_client.HTTPClient(distil_url=self.distil_url)
        client.get_usage(self.tenant, self.start, self.end)
        mock_get.assert_called_once_with('http://127.0.0.1:9999/get_usage',
                                         headers={'X-Auth-Token':
                                                  'fake_token'},
                                         params={'tenant': 'fake_tenant',
                                                 'end': '2017-02-01',
                                                 'start': '2017-01-01'},
                                         verify=True)
