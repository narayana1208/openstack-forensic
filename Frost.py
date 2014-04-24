# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
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

import datetime
import urlparse

from webob import exc

from nova.api.openstack import extensions
from nova.api.openstack import wsgi
from nova.api.openstack import xmlutil
from nova.compute import api
from nova import exception
from nova import flags

LOG  =  logging . getLogger(__name__)
authorize  =  extensions . extension_authorizer('compute', 'Frost')
authorize_all_tenants  =  extensions . extension_authorizer('compute','frost:all_tenants')
FLAGS = flags.FLAGS

Frost = [{'id': 1,
         'type': 'cute', 'thumb':
         'http://images.ansolabs.com/coco.jpg',
         'url': 'http://pages.swcp.com/~jamii/OtherCats/'},
        {'id': 2,
         'type': 'funny',
         'thumb': 'http://images.ansolabs.com/funny-cat.jpg',
         'url': 'http://www.hilariouspetvideos.com/'},
]


class FrostController(object):
    """Simple cat resource"""

    def index(self, req):
        """Retrieve a list of cats"""
        context = req.environ['nova.context']

        return {'Frost': FROST}

    def show(self, req, id):
        """Show a specific cat"""
        # FIXME: Make this return the proper cat!
        raise exc.HTTPNotImplemented()


class ExtendedServerCatController(wsgi.Controller):
    """Simple Frost server extension"""
    @wsgi.extends
    def show(self, req, resp_obj, id):
        # FIXME: Make this return a random cat!
        resp_obj.obj['server']['cat'] = {}


class Frost(extensions.ExtensionDescriptor):
    """Simple cat extension"""

    name = "Frost"
    alias = "os-frost"
    namespace = ("http://docs.openstack.org/compute/ext/"
                 "os-frost/api/v1.1")
    updated = "2012-03-20T00:00:00+00:00"

    def get_resources(self):
        """Return list of resource extensions"""
        resources = []

        res = extensions.ResourceExtension('os-frost',
                                           FrostController())
        resources.append(res)
        return resources

    def get_controller_extensions(self):
        """Return list of controller extensions"""
        controller = ExtendedServerCatController()
        extension = extensions.ControllerExtension(self, 'servers', controller)
        return [extension]
