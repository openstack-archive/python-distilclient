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

    def list(self, project_id=None, detailed=False):
        """Retrieve a list of quotations.

        :param project_id: Project ID, there there is no project id given,
                           Distil will use the project ID from token.
        :param detailed: Default value is False, indicate if inlucding detailed
                         usage info in the response.
        :returns: A list of quotations.
        """

        url = "/v2/quotations?detailed=" + str(detailed)
        if project_id:
            url = url + "&project_id=" + project_id
        return self._list(url, "quotations")
