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


import exc
import json
import os
import sys

from keystoneauth1.identity import generic
from keystoneauth1 import session

from client import Client


def main():
    import argparse
    parser = argparse.ArgumentParser()

    # main args:
    parser.add_argument('-k', '--insecure',
                        default=False,
                        action='store_true',
                        help="Explicitly allow distilclient to "
                        "perform \"insecure\" SSL (https) requests. "
                        "The server's certificate will "
                        "not be verified against any certificate "
                        "authorities. This option should be used with "
                        "caution.")

    parser.add_argument('--os-cacert',
                        metavar='<ca-certificate-file>',
                        dest='os_cacert',
                        help='Path of CA TLS certificate(s) used to verify'
                        'the remote server\'s certificate. Without this '
                        'option distil looks for the default system '
                        'CA certificates.')

    parser.add_argument('--os-username',
                        default=os.environ.get('OS_USERNAME'),
                        help='Defaults to env[OS_USERNAME]')

    parser.add_argument('--os-password',
                        default=os.environ.get('OS_PASSWORD'),
                        help='Defaults to env[OS_PASSWORD]')

    parser.add_argument('--os-project-id',
                        default=os.environ.get(
                            'OS_PROJECT_ID', os.environ.get(
                                'OS_TENANT_ID')),
                        help='Defaults to env[OS_PROJECT_ID]')

    parser.add_argument('--os-project-name',
                        default=os.environ.get(
                            'OS_PROJECT_NAME', os.environ.get(
                                'OS_TENANT_NAME')),
                        help='Defaults to env[OS_PROJECT_NAME]')

    parser.add_argument('--os-project-domain-id',
                        default=os.environ.get('OS_PROJECT_DOMAIN_ID'),
                        help='Defaults to env[OS_PROJECT_DOMAIN_ID]')

    parser.add_argument('--os-project-domain-name',
                        default=os.environ.get('OS_PROJECT_DOMAIN_NAME'),
                        help='Defaults to env[OS_PROJECT_DOMAIN_NAME]')

    parser.add_argument('--os-user-domain-id',
                        default=os.environ.get('OS_USER_DOMAIN_ID'),
                        help='Defaults to env[OS_USER_DOMAIN_ID]')

    parser.add_argument('--os-user-domain-name',
                        default=os.environ.get('OS_USER_DOMAIN_NAME'),
                        help='Defaults to env[OS_USER_DOMAIN_NAME]')

    parser.add_argument('--os-auth-url',
                        default=os.environ.get('OS_AUTH_URL'),
                        help='Defaults to env[OS_AUTH_URL]')

    parser.add_argument('--os-region-name',
                        default=os.environ.get('OS_REGION_NAME'),
                        help='Defaults to env[OS_REGION_NAME]')

    parser.add_argument('--os-token',
                        default=os.environ.get('OS_TOKEN'),
                        help='Defaults to env[OS_TOKEN]')

    parser.add_argument('--os-service-type',
                        help='Defaults to env[OS_SERVICE_TYPE].',
                        default='rating')

    parser.add_argument('--os-endpoint-type',
                        help='Defaults to env[OS_ENDPOINT_TYPE].',
                        default='publicURL')

    parser.add_argument("--distil-url",
                        help="Distil endpoint, defaults to env[DISTIL_URL]",
                        default=os.environ.get('DISTIL_URL'))

    # commands:
    subparsers = parser.add_subparsers(help='commands', dest='command')

    subparsers.add_parser(
        'collect-usage', help=('process usage for all tenants'))

    subparsers.add_parser(
        'last-collected', help=('get last collected time'))

    get_usage_parser = subparsers.add_parser(
        'get-usage', help=('get raw aggregated usage'))

    get_usage_parser.add_argument(
        "-p", "--project", dest="project",
        help='Tenant to get usage for',
        required=True)

    get_usage_parser.add_argument(
        "-s", "--start", dest="start",
        help="Start time",
        required=True)

    get_usage_parser.add_argument(
        "-e", "--end", dest="end",
        help="End time",
        required=True)

    get_rated_parser = subparsers.add_parser(
        'get-rated', help=('get rated usage'))

    get_rated_parser.add_argument(
        "-p", "--project", dest="project",
        help='Tenant to get usage for',
        required=True)

    get_rated_parser.add_argument(
        "-s", "--start", dest="start",
        help="Start time",
        required=True)

    get_rated_parser.add_argument(
        "-e", "--end", dest="end",
        help="End time")

    args = parser.parse_args()

    if not (args.os_token and args.distil_url):
        if not args.os_username:
            raise exc.CommandError("You must provide a username via "
                                   "either --os-username or via "
                                   "env[OS_USERNAME]")

        if not (args.os_project_id or args.os_project_name):
            raise exc.CommandError(
                "You must provide a a project id via either --os-project-id "
                "or env[OS_PROJECT_ID] or a project name via "
                "either --os-project-name or env[OS_PROJECT_NAME]")

        if not args.os_auth_url:
            raise exc.CommandError(
                "You must provide an auth url via "
                "either --os-auth-url or via "
                "env[OS_AUTH_URL]")

        if not args.os_password and not args.os_token:
            raise exc.CommandError(
                "You must provide a password via "
                "either --os-password or via "
                "env[OS_PASSWORD] or an auth token "
                "via --os-token or env[OS_TOKEN]")

    if args.insecure:
        verify = False
    else:
        verify = args.os_cacert or True

    if args.os_token and args.distil_url:
        client = Client(
            endpoint=args.distil_url,
            token=args.os_token)
    else:
        if args.os_token:
            kwargs = {
                'token': args.os_token,
                'auth_url': args.os_auth_url,
                'username': args.os_username,
                'project_id': args.os_project_id,
                'project_name': args.os_project_name,
                'project_domain_id': args.os_project_domain_id,
                'project_domain_name': args.os_project_domain_name,
            }
            auth = generic.Token(**kwargs)
            sess = session.Session(auth=auth, verify=verify)
        else:
            kwargs = {
                'username': args.os_username,
                'password': args.os_password,
                'auth_url': args.os_auth_url,
                'project_id': args.os_project_id,
                'project_name': args.os_project_name,
                'project_domain_id': args.os_project_domain_id,
                'project_domain_name': args.os_project_domain_name,
                'user_domain_id': args.os_user_domain_id,
                'user_domain_name': args.os_user_domain_name,
            }
            auth = generic.Password(**kwargs)
            sess = session.Session(auth=auth, verify=verify)

        endpoint = auth.get_endpoint(
            sess, service_type=args.os_service_type,
            interface=args.os_endpoint_type, region_name=args.os_region_name)

        kwargs = {
            'endpoint': endpoint,
            'auth_url': args.os_auth_url,
            'session': sess,
            'auth': auth,
            'service_type': args.os_service_type,
            'endpoint_type': args.os_endpoint_type,
            'region_name': args.os_region_name,
            'username': args.os_username,
            'password': args.os_password,
        }

        client = Client(**kwargs)

    if args.command == 'collect-usage':
        response = client.collect_usage()
        print(json.dumps(response, indent=2))

    if args.command == 'last-collected':
        response = client.last_collected()
        print(json.dumps(response, indent=2))

    if args.command == 'get-usage':
        response = client.get_usage(args.project, args.start, args.end)
        print(json.dumps(response, indent=2))

    if args.command == 'get-rated':
        response = client.get_rated(args.project, args.start, args.end)
        print(json.dumps(response, indent=2))


if __name__ == '__main__':
    main(sys.argv[1:])
