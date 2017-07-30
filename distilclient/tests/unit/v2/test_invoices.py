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

import datetime
import mock

import distilclient
from distilclient import base
from distilclient.tests.unit import utils
from distilclient.v2 import client

from oslo_utils import uuidutils


class InvoicesTest(utils.TestCase):

    def setUp(self):
        super(InvoicesTest, self).setUp()
        self.client = client.Client(session=client.session.Session(),
                                    api_version=distilclient.API_MAX_VERSION,
                                    distil_url=uuidutils.generate_uuid(),
                                    retries=3,
                                    input_auth_token='token')

    @mock.patch.object(base.Manager, '_list')
    def test_list_with_project_id(self, mock_list):
        self.client.invoices.list('2017-1-1', '2018-2-1',
                                  'project_id')
        mock_list.assert_called_with('/v2/invoices?start=2017-1-1'
                                     '&end=2018-2-1&detailed=False&'
                                     'project_id=project_id',
                                     'invoices')

    @mock.patch.object(base.Manager, '_list')
    def test_list_without_project_id(self, mock_list):
        self.client.invoices.list('2017-1-1', '2018-2-1')
        mock_list.assert_called_with('/v2/invoices?start=2017-1-1'
                                     '&end=2018-2-1&detailed=False',
                                     'invoices')

    @mock.patch.object(base.Manager, '_list')
    def test_list_with_datetime(self, mock_list):
        start = datetime.date(year=2017, day=1, month=1)
        end = datetime.date(year=2018, day=1, month=2)
        self.client.invoices.list(start, end,
                                  'project_id')
        mock_list.assert_called_with('/v2/invoices?start=2017-01-01'
                                     '&end=2018-02-01&detailed=False'
                                     '&project_id=project_id', 'invoices')
