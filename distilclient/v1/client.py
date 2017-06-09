# Copyright (C) 2014 Catalyst IT Ltd
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

import requests
from requests.exceptions import ConnectionError

import six.moves.urllib.parse as urlparse

from keystoneauth1 import adapter
from keystoneauth1.identity import generic
from keystoneauth1 import session


def Client(session=None, endpoint=None, username=None, password=None,
           include_pass=None, endpoint_type=None,
           auth_url=None, **kwargs):
    if session:
        kwargs['endpoint_override'] = endpoint
        return SessionClient(session, **kwargs)
    else:
        return HTTPClient(**kwargs)


class SessionClient(object):
    """HTTP client based on Keystone client session."""

    def __init__(self, session, service_type='rating',
                 interface='publicURL', **kwargs):

        self.client = adapter.LegacyJsonAdapter(
            session, service_type=service_type, interface=interface, **kwargs)

    def collect_usage(self):

        headers = {"Content-Type": "application/json"}

        response, json = self.client.request(
            "collect_usage", 'POST', headers=headers)
        if response.status_code != 200:
            raise AttributeError("Usage cycle failed: %s  code: %s" %
                                 (response.text, response.status_code))
        else:
            return json

    def last_collected(self):

        headers = {"Content-Type": "application/json"}

        response, json = self.client.request(
            "last_collected", 'GET', headers=headers)
        if response.status_code != 200:
            raise AttributeError("Get last collected failed: %s code: %s" %
                                 (response.text, response.status_code))
        else:
            return json

    def get_usage(self, tenant, start, end):
        return self._query_usage(tenant, start, end, "get_usage")

    def get_rated(self, tenant, start, end):
        return self._query_usage(tenant, start, end, "get_rated")

    def _query_usage(self, tenant, start, end, url):

        params = {"tenant": tenant,
                  "start": start,
                  "end": end
                  }

        response, json = self.client.request(
            url, 'GET', params=params)
        if response.status_code != 200:
            raise AttributeError("Get usage failed: %s code: %s" %
                                 (response.text, response.status_code))
        else:
            return json


class HTTPClient(object):

    def __init__(self, distil_url=None, os_auth_token=None,
                 os_username=None, os_password=None,
                 os_project_id=None, os_project_name=None,
                 os_tenant_id=None, os_tenant_name=None,
                 os_project_domain_id='default',
                 os_project_domain_name='Default',
                 os_auth_url=None, os_region_name=None,
                 os_cacert=None, insecure=False,
                 os_service_type='rating', os_endpoint_type='publicURL'):

        project_id = os_project_id or os_tenant_id
        project_name = os_project_name or os_tenant_name

        self.insecure = insecure

        if os_auth_token and distil_url:
            self.auth_token = os_auth_token
            self.endpoint = distil_url
        else:
            if insecure:
                verify = False
            else:
                verify = os_cacert or True

            kwargs = {
                'username': os_username,
                'password': os_password,
                'auth_url': os_auth_url,
                'project_id': project_id,
                'project_name': project_name,
                'project_domain_id': os_project_domain_id,
                'project_domain_name': os_project_domain_name,
            }
            auth = generic.Password(**kwargs)
            sess = session.Session(auth=auth, verify=verify)

            if os_auth_token:
                self.auth_token = os_auth_token
            else:
                self.auth_token = auth.get_token(sess)

            if distil_url:
                self.endpoint = distil_url
            else:
                self.endpoint = auth.get_endpoint(
                    sess, service_type=os_service_type,
                    interface=os_endpoint_type,
                    region_name=os_region_name)

    def collect_usage(self):
        url = urlparse.urljoin(self.endpoint, "collect_usage")

        headers = {"Content-Type": "application/json",
                   "X-Auth-Token": self.auth_token}

        try:
            response = requests.post(url, headers=headers,
                                     verify=not self.insecure)
            if response.status_code != 200:
                raise AttributeError("Usage cycle failed: %s  code: %s" %
                                     (response.text, response.status_code))
            else:
                return response.json()
        except ConnectionError as e:
            print(e)

    def last_collected(self):
        url = urlparse.urljoin(self.endpoint, "last_collected")

        headers = {"Content-Type": "application/json",
                   "X-Auth-Token": self.auth_token}

        try:
            response = requests.get(url, headers=headers,
                                    verify=not self.insecure)
            if response.status_code != 200:
                raise AttributeError("Get last collected failed: %s code: %s" %
                                     (response.text, response.status_code))
            else:
                return response.json()
        except ConnectionError as e:
            print(e)

    def get_usage(self, tenant, start, end):
        return self._query_usage(tenant, start, end, "get_usage")

    def get_rated(self, tenant, start, end):
        return self._query_usage(tenant, start, end, "get_rated")

    def _query_usage(self, tenant, start, end, endpoint):
        url = urlparse.urljoin(self.endpoint, endpoint)

        headers = {"X-Auth-Token": self.auth_token}

        params = {"tenant": tenant,
                  "start": start,
                  "end": end
                  }

        try:
            response = requests.get(url, headers=headers,
                                    params=params,
                                    verify=not self.insecure)
            if response.status_code != 200:
                raise AttributeError("Get usage failed: %s code: %s" %
                                     (response.text, response.status_code))
            else:
                return response.json()
        except ConnectionError as e:
            print(e)
