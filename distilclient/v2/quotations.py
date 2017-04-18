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

from distilclient import base


class QuotationManager(base.Manager):

    def list(self, start, end, project_id=None):
        """Retrieve a list of quotations.

        :param start: Start date of the query
        :param end: End date of the query
        :param project_id: Project ID, there there is no project id given,
                           Distil will use the project ID from token.
        :returns: A list of quotations.
        """

        url = "/v2/quotations?start={0}&end={1}"
        if project_id:
            url = url.format(start, end) + "&project_id=" + project_id
        else:
            url = url.format(start, end)

        return self._list(url, "quotations")
