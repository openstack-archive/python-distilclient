# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2011 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

from distilclient.tests.unit.v2 import fake_clients as fakes
from distilclient.v2 import client


class FakeClient(fakes.FakeClient):

    def __init__(self, *args, **kwargs):
        client.Client.__init__(
            self,
            '2',
            'username',
            'password',
            'project_id',
            'auth_url',
            input_auth_token='token',
            extensions=kwargs.get('extensions'),
            distil_url='http://localhost:9999',
            api_version=kwargs.get("api_version", '2')
        )
        self.client = FakeHTTPClient(**kwargs)


def get_fake_export_location():
    return {
        'uuid': 'foo_el_uuid',
        'path': '/foo/el/path',
        'share_instance_id': 'foo_share_instance_id',
        'is_admin_only': False,
        'created_at': '2015-12-17T13:14:15Z',
        'updated_at': '2015-12-17T14:15:16Z',
    }


def get_fake_snapshot_export_location():
    return {
        'uuid': 'foo_el_uuid',
        'path': '/foo/el/path',
        'share_snapshot_instance_id': 'foo_share_instance_id',
        'is_admin_only': False,
        'created_at': '2017-01-17T13:14:15Z',
        'updated_at': '2017-01-17T14:15:16Z',
    }


class FakeHTTPClient(fakes.FakeHTTPClient):

    def get_(self, **kw):
        body = {
            "versions": [
                {
                    "status": "CURRENT",
                    "updated": "2015-07-30T11:33:21Z",
                    "links": [
                        {
                            "href": "http://docs.openstack.org/",
                            "type": "text/html",
                            "rel": "describedby",
                        },
                        {
                            "href": "http://localhost:8786/v2/",
                            "rel": "self",
                        }
                    ],
                    "min_version": "2.0",
                    "version": self.default_headers[
                        "X-Openstack-Distil-Api-Version"],
                    "id": "v2.0",
                }
            ]
        }
        return (200, {}, body)

    def get_availability_zones(self):
        availability_zones = {
            "availability_zones": [
                {"id": "368c5780-ad72-4bcf-a8b6-19e45f4fafoo",
                 "name": "foo",
                 "created_at": "2016-07-08T14:13:12.000000",
                 "updated_at": "2016-07-08T15:14:13.000000"},
                {"id": "368c5780-ad72-4bcf-a8b6-19e45f4fabar",
                 "name": "bar",
                 "created_at": "2016-07-08T14:13:12.000000",
                 "updated_at": "2016-07-08T15:14:13.000000"},
            ]
        }
        return (200, {}, availability_zones)

    def get_os_services(self, **kw):
        services = {
            "services": [
                {"status": "enabled",
                 "binary": "distil-scheduler",
                 "zone": "foozone",
                 "state": "up",
                 "updated_at": "2015-10-09T13:54:09.000000",
                 "host": "lucky-star",
                 "id": 1},
                {"status": "enabled",
                 "binary": "distil-share",
                 "zone": "foozone",
                 "state": "up",
                 "updated_at": "2015-10-09T13:54:05.000000",
                 "host": "lucky-star",
                 "id": 2},
            ]
        }
        return (200, {}, services)

    get_services = get_os_services

    def put_os_services_enable(self, **kw):
        return (200, {}, {'host': 'foo', 'binary': 'distil-share',
                          'disabled': False})

    put_services_enable = put_os_services_enable

    def put_os_services_disable(self, **kw):
        return (200, {}, {'host': 'foo', 'binary': 'distil-share',
                          'disabled': True})

    put_services_disable = put_os_services_disable

    def get_v2(self, **kw):
        body = {
            "versions": [
                {
                    "status": "CURRENT",
                    "updated": "2015-07-30T11:33:21Z",
                    "links": [
                        {
                            "href": "http://docs.openstack.org/",
                            "type": "text/html",
                            "rel": "describedby",
                        },
                        {
                            "href": "http://localhost:8786/v2/",
                            "rel": "self",
                        }
                    ],
                    "min_version": "2.0",
                    "version": "2.5",
                    "id": "v1.0",
                }
            ]
        }
        return (200, {}, body)

    def get_shares_1234(self, **kw):
        share = {'share': {'id': 1234, 'name': 'sharename'}}
        return (200, {}, share)
