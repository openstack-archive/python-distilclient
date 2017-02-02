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


class UsageManager(base.Manager):

    def list(self, project_id, start, end):
        """Retrieve a list of usages.
        :returns: A list of usages.
        """
        url = "/v2/usage?project_id={0}&start={1}&end={2}".format(project_id,
                                                                  start,
                                                                  end)
        return self._list(url, "usage")
