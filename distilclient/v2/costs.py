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


class CostManager(base.Manager):

    def list(self, start, end, project_id=None):
        """Retrieve a list of costs.
        :returns: A list of costs.
        """
        url = "/v2/costs?start={1}&end={2}"
        if project_id:
            url = url.format(start, end) + "&project_id=" + project_id
        else:
            url = url.format(start, end)

        return self._list(url, "costs")
