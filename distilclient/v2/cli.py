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
