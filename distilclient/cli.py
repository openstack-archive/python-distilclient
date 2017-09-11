# Copyright 2017 Catalyst IT Ltd.
#
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

import logging

from osc_lib import utils

LOG = logging.getLogger(__name__)

DEFAULT_OS_RATING_API_VERSION = '2'
API_VERSION_OPTION = 'os_rating_api_version'
API_NAME = "rating"
API_VERSIONS = {
    "2": "distilclient.v2.client.Client",
}


def make_client(instance):
    """Returns an distil service client"""
    distil_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)

    LOG.debug("Instantiating distil client: {0}".format(
        distil_client))

    kwargs = {
        'session': instance.session,
        'service_type': 'ratingv2',
        'region_name': instance._region_name
    }

    distil_endpoint = instance.get_configuration().get('distil_url')
    if not distil_endpoint:
        distil_endpoint = instance.get_endpoint_for_service_type(
            'ratingv2',
            region_name=instance._region_name,
            interface=instance._interface
        )

    client = distil_client(distil_endpoint, **kwargs)
    return client


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-rating-api-version',
        metavar='<os-rating-api-version>',
        default=utils.env(
            'OS_RATING_API_VERSION',
            default=DEFAULT_OS_RATING_API_VERSION),
        help=('Client version, default=' +
              DEFAULT_OS_RATING_API_VERSION +
              ' (Env: OS_RATING_API_VERSION)'))
    return parser
