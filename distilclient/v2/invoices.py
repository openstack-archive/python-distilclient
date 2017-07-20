# Copyright 2017 Catalyst IT Ltd.
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

import datetime
from distilclient import base


class InvoiceManager(base.Manager):

    def list(self, start, end, project_id=None, detailed=False):
        """Retrieve a list of invoices.

        :param start: Start date of the query
        :param end: End date of the query
        :param project_id: Project ID, there there is no project id given,
                           Distil will use the project ID from token.
        :param detailed: Default value is False, indicate if inlucding detailed
                         usage info in the response.
        :returns: A list of invoices.
        """
        if isinstance(start, datetime.datetime):
            start = start.strftime('%Y-%m-%d')
        if isinstance(end, datetime.datetime):
            end = end.strftime('%Y-%m-%d')

        url = "/v2/invoices?start={0}&end={1}&detailed={2}"
        if project_id:
            url = (url.format(start, end, detailed) +
                   "&project_id=" + project_id)
        else:
            url = url.format(start, end, detailed)

        return self._list(url, "invoices")
