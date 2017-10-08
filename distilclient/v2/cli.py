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

from collections import namedtuple
import datetime
import json

from osc_lib.command import command
from osc_lib import utils
from oslo_log import log as logging

from distilclient.i18n import _


class Health(command.Lister):
    """Display detailed health status of Distil server"""

    _description = _("Display detailed health status of Distil server")
    log = logging.getLogger(__name__ + ".Health")

    def take_action(self, parsed_args):
        health = self.app.client_manager.rating.health.get()
        columns = ("Indicator", "Status", "Message")
        indicators = []
        for k in health["health"].keys():
            indicators.append({"indicator": k,
                               "status": health["health"][k]["status"],
                               "message": health["health"][k]["msg"]})
        rows = (utils.get_item_properties(namedtuple('GenericDict',
                                                     i.keys())(**i), columns)
                for i in indicators)

        return (columns, rows)


class ListProducts(command.Lister):
    """List available products"""

    _description = _("List available products")
    log = logging.getLogger(__name__ + ".ListProducts")

    def get_parser(self, prog_name):
        parser = super(ListProducts, self).get_parser(prog_name)
        parser.add_argument(
            "--regions",
            metavar="<regions>",
            help="Region list separated with commas.")

        return parser

    def take_action(self, parsed_args):
        kwargs = {}
        columns = ("Region", "Category", "Name", "Rate", "Unit")
        if parsed_args.regions is not None:
            kwargs["regions"] = parsed_args.regions.split(',')

        data = self.app.client_manager.rating.products.list(**kwargs)
        products = []
        for region in data["products"].keys():
            for category in data["products"][region].keys():
                for product in data["products"][region][category]:
                    formated_product = product.copy()
                    formated_product["region"] = region
                    formated_product["category"] = category
                    products.append(formated_product)

        rows = (utils.get_item_properties(namedtuple('GenericDict',
                                                     p.keys())(**p), columns)
                for p in products)
        return (columns, rows)


class ListQuotations(command.Command):
    """Show current month quotation.

    NOTE: The quotations API only shows data from current region for current
          month.
    """

    _description = _("List available quotations")
    log = logging.getLogger(__name__ + ".ListQuotations")

    def get_parser(self, prog_name):
        parser = super(ListQuotations, self).get_parser(prog_name)
        parser.add_argument(
            "--detailed",
            action="store_true",
            help="Whether get the details of current month quotation.")

        parser.add_argument(
            "--project-id",
            help="Only admin user can specify the project ID.")

        parser.add_argument(
            "--original-json",
            action="store_true",
            help="Whether print out the original JSON response directly.")

        return parser

    def take_action(self, parsed_args):
        kwargs = {}
        if parsed_args.detailed is not None:
            kwargs["detailed"] = parsed_args.detailed

        if parsed_args.project_id is not None:
            kwargs["project_id"] = parsed_args.project_id

        data = self.app.client_manager.rating.quotations.list(**kwargs)

        print(json.dumps(data, indent=4, sort_keys=True))


class ListInvoices(command.Command):
    """List available invoices. """

    _description = _("List available invoices")
    log = logging.getLogger(__name__ + ".ListInvoices")

    def get_parser(self, prog_name):
        parser = super(ListInvoices, self).get_parser(prog_name)
        parser.add_argument(
            "--start",
            required=True,
            help="The start date of time range to get invoices.")

        parser.add_argument(
            "--end",
            help="The end date of time range to get invoices.")

        parser.add_argument(
            "--detailed",
            action="store_true",
            help="Whether get the details of current month quotation.")

        parser.add_argument(
            "--project-id",
            help="Only admin user can specify the project ID.")

        return parser

    def take_action(self, parsed_args):
        kwargs = {}

        if parsed_args.start is not None:
            kwargs["start"] = parsed_args.start

        if parsed_args.end is not None:
            kwargs["end"] = parsed_args.end
        else:
            kwargs["end"] = datetime.datetime.now()

        if parsed_args.detailed is not None:
            kwargs["detailed"] = parsed_args.detailed

        if parsed_args.project_id is not None:
            kwargs["project_id"] = parsed_args.project_id

        data = self.app.client_manager.rating.invoices.list(**kwargs)

        print(json.dumps(data, indent=4, sort_keys=True))
