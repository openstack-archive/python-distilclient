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

from six.moves.urllib import parse

from zunclient.common import base
from zunclient.common import utils
from zunclient import exceptions


class Usage(base.Resource):
    def __repr__(self):
        return "<Usage %s>" % self._info


class UsageManager(base.Manager):
    resource_class = Usage

    @staticmethod
    def _path(id=None):
        return '/v2/usages'

    def list(self, marker=None, limit=None, sort_key=None,
             sort_dir=None, detail=False):
        """Retrieve a list of usages.
        :returns: A list of usages.
        """
        if limit is not None:
            limit = int(limit)

        filters = utils.common_filters(marker, limit, sort_key, sort_dir)

        path = ''
        if detail:
            path += 'detail'
        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path),
                              "usages")
        else:
            return self._list_pagination(self._path(path),
                                         "usages",
                                         limit=limit)
