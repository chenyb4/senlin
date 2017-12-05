# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg
from oslo_log import log
from openstack import connection
from openstack import exceptions
from openstack import profile

from senlin.common.i18n import _LW
from senlin.drivers import base
from senlin.drivers.openstack import sdk

LOG = log.getLogger(__name__)


class NovaClient(base.DriverBase):
    '''Nova V2 driver.'''

    def __init__(self, params):
        super(NovaClient, self).__init__(params)
        self.conn = sdk.create_connection(params)
        self.session = self.conn.session

    @sdk.translate_exception
    def flavor_create(self, **attrs):
        return self.conn.compute.create_flavor(**attrs)

    @sdk.translate_exception
    def flavor_get(self, flavor):
        return self.conn.compute.get_flavor(flavor)

    @sdk.translate_exception
    def flavor_find(self, name_or_id, ignore_missing=False):
        return self.conn.compute.find_flavor(name_or_id, ignore_missing)

    @sdk.translate_exception
    def flavor_list(self, details=True, **query):
        return self.conn.compute.flavors(details, **query)

    @sdk.translate_exception
    def flavor_update(self, flavor, **attrs):
        return self.conn.compute.update_flavor(flavor, **attrs)

    @sdk.translate_exception
    def flavor_delete(self, flavor, ignore_missing=True):
        return self.conn.compute.delete_flavor(flavor, ignore_missing)

    @sdk.translate_exception
    def image_get(self, image):
        return self.conn.compute.get_image(image)

    @sdk.translate_exception
    def image_find(self, name_or_id, ignore_missing=False):
        return self.conn.compute.find_image(name_or_id, ignore_missing)

    @sdk.translate_exception
    def image_list(self, details=True, **query):
        return self.conn.compute.images(details, **query)

    @sdk.translate_exception
    def image_delete(self, image, ignore_missing=True):
        return self.conn.compute.delete_image(image, ignore_missing)

    @sdk.translate_exception
    def keypair_create(self, **attrs):
        return self.conn.compute.create_keypair(**attrs)

    @sdk.translate_exception
    def keypair_get(self, image):
        return self.conn.compute.get_keypair(image)

    @sdk.translate_exception
    def keypair_find(self, name_or_id, ignore_missing=False):
        return self.conn.compute.find_keypair(name_or_id, ignore_missing)

    @sdk.translate_exception
    def keypair_list(self, **query):
        return self.conn.compute.keypairs(**query)

    @sdk.translate_exception
    def keypair_update(self, keypair, **attrs):
        return self.conn.compute.update_keypair(keypair, **attrs)

    @sdk.translate_exception
    def keypair_delete(self, keypair, ignore_missing=True):
        return self.conn.compute.delete_keypair(keypair, ignore_missing)

    @sdk.translate_exception
    def server_create(self, **attrs):
        server_obj = self.conn.compute.create_server(**attrs)
        return server_obj

    @sdk.translate_exception
    def server_get(self, server):
        return self.conn.compute.get_server(server)

    @sdk.translate_exception
    def server_list(self, details=True, **query):
        return self.conn.compute.servers(details, **query)

    @sdk.translate_exception
    def server_update(self, server, **attrs):
        return self.conn.compute.update_server(server, **attrs)

    @sdk.translate_exception
    def server_delete(self, server, ignore_missing=True):
        return self.conn.compute.delete_server(server,
                                               ignore_missing=ignore_missing)

    @sdk.translate_exception
    def server_force_delete(self, server, ignore_missing=True):
        try:
            sv = self.conn.compute.delete_server(server,
                                                 ignore_missing=ignore_missing,
                                                 force=True)
            return sv
        except exceptions.NotFoundException:
            LOG.warning(_LW("No server with a name or ID of %s exists."
                            % (server)))

    @sdk.translate_exception
    def server_rebuild(self, server, image, name=None, admin_password=None,
                       **attrs):
        return self.conn.compute.rebuild_server(server, name, admin_password,
                                                image=image, **attrs)

    @sdk.translate_exception
    def server_resize(self, server, flavor):
        return self.conn.compute.resize_server(server, flavor)

    @sdk.translate_exception
    def server_resize_confirm(self, server):
        return self.conn.compute.confirm_resize_server(server)

    @sdk.translate_exception
    def server_resize_revert(self, server):
        return self.conn.compute.revert_resize_server(server)

    @sdk.translate_exception
    def server_reboot(self, server, reboot_type):
        return self.conn.compute.reboot_server(server, reboot_type)

    @sdk.translate_exception
    def server_change_password(self, server, new_password):
        return self.conn.compute.change_server_password(server, new_password)

    @sdk.translate_exception
    def wait_for_server(self, server, status='ACTIVE', failures=['ERROR'],
                        interval=2, timeout=None):
        '''Wait for server creation complete'''
        if timeout is None:
            timeout = cfg.CONF.default_action_timeout

        server_obj = self.conn.compute.find_server(server, False)
        self.conn.compute.wait_for_server(server_obj, status=status,
                                          failures=failures,
                                          interval=interval,
                                          wait=timeout)
        return

    @sdk.translate_exception
    def wait_for_server_delete(self, server, timeout=None):
        '''Wait for server deleting complete'''
        if timeout is None:
            timeout = cfg.CONF.default_action_timeout

        server_obj = self.conn.compute.find_server(server, True)
        if server_obj:
            self.conn.compute.wait_for_delete(server_obj, wait=timeout)

        return

    @sdk.translate_exception
    def server_interface_create(self, server, **attrs):
        return self.conn.compute.create_server_interface(server, **attrs)

    @sdk.translate_exception
    def server_interface_get(self, interface, server):
        return self.conn.compute.get_server_interface(interface, server)

    @sdk.translate_exception
    def server_interface_list(self, server, **query):
        return self.conn.compute.server_interfaces(server, **query)

    @sdk.translate_exception
    def server_interface_delete(self, interface, server, ignore_missing=True):
        return self.conn.compute.delete_server_interface(interface, server,
                                                         ignore_missing)

    @sdk.translate_exception
    def server_ip_list(self, **query):
        return self.conn.compute.server_ips(**query)

    @sdk.translate_exception
    def server_metadata_create(self, server, metadata):
        self.conn.compute.set_server_metadata(server, **metadata)

    @sdk.translate_exception
    def server_metadata_get(self, server):
        res = self.conn.compute.get_server_metadata(server)
        return res.metadata

    @sdk.translate_exception
    def server_metadata_update(self, server, metadata):
        # Clean all existing metadata first
        res = self.conn.compute.get_server_metadata(server)
        if res.metadata:
            self.conn.compute.delete_server_metadata(
                server, list(res.metadata.keys()))

        # Then reset metadata to given value if it is not {}
        if metadata:
            return self.conn.compute.set_server_metadata(server, **metadata)

    @sdk.translate_exception
    def server_metadata_delete(self, server, keys):
        self.conn.compute.delete_server_metadata(server, keys)

    @sdk.translate_exception
    def availability_zone_list(self, **query):
        return self.conn.compute.availability_zones(**query)

    def validate_azs(self, azs):
        """check whether availability zones provided are valid.

        :param azs: A list of availability zone names for checking.
        :returns: A list of zones that are found available on Nova.
        """
        known = self.availability_zone_list()
        names = [az['zoneName'] for az in known
                 if az['zoneState']['available']]

        found = []
        for az in azs:
            if az in names:
                found.append(az)
            else:
                LOG.warning(_LW("Availability zone '%s' is not available."),
                            az)
        return found

    @sdk.translate_exception
    def server_group_create(self, **attrs):
        return self.conn.compute.create_server_group(**attrs)

    @sdk.translate_exception
    def server_group_delete(self, server_group, ignore_missing=True):
        return self.conn.compute.delete_server_group(
            server_group, ignore_missing=ignore_missing)

    @sdk.translate_exception
    def server_group_find(self, name_or_id, ignore_missing=True):
        return self.conn.compute.find_server_group(
            name_or_id, ignore_missing=ignore_missing)

    @sdk.translate_exception
    def server_group_get(self, server_group):
        return self.conn.compute.get_server_group(server_group)

    @sdk.translate_exception
    def server_group_list(self, **query):
        return self.conn.compute.server_groups(**query)

    @sdk.translate_exception
    def hypervisor_list(self, **query):
        return self.conn.compute.hypervisors(**query)

    @sdk.translate_exception
    def hypervisor_find(self, name_or_id, ignore_missing=True):
        return self.conn.compute.find_hypervisor(
            name_or_id, ignore_missing=ignore_missing)

    @sdk.translate_exception
    def hypervisor_get(self, hypervisor):
        return self.conn.compute.get_hypervisor(hypervisor)

    @sdk.translate_exception
    def service_list(self):
        return self.conn.compute.services()

    @sdk.translate_exception
    def service_force_down(self, service):
        return self.conn.compute.force_service_down(service, service.host,
                                                    service.binary)

    @sdk.translate_exception
    def service_enable(self, service):
        return self.conn.compute.enable_service(service, service.host,
                                                service.binary)

    @sdk.translate_exception
    def service_disable(self, service, disabled_reason=None):
        return self.conn.compute.disable_service(service,
                                                 service.host,
                                                 service.binary,
                                                 disabled_reason)

    @sdk.translate_exception
    def server_floatingip_associate(self, server, address):
        return self.conn.compute.add_floating_ip_to_server(server, address)

    @sdk.translate_exception
    def server_floatingip_disassociate(self, server, address):
        return self.conn.compute.remove_floating_ip_from_server(server,
                                                                address)

    @sdk.translate_exception
    def create_volume_attachment(self, server, **attr):
        return self.conn.compute.create_volume_attachment(server, **attr)

    @sdk.translate_exception
    def delete_volume_attachment(self, volume_id, server, ignore_missing=True):
        return self.conn.compute.delete_volume_attachment(
            volume_id, server, ignore_missing=ignore_missing
        )

    @sdk.translate_exception
    def server_state_reset(self, server, state=None):
        auth_url = cfg.CONF.authentication.auth_url
        region = cfg.CONF.default_region_name
        project_name = cfg.CONF.authentication.service_project_name
        user_domain_name = cfg.CONF.authentication.service_user_domain
        project_domain_name = cfg.CONF.authentication.service_project_domain
        username = cfg.CONF.authentication.service_username
        password = cfg.CONF.authentication.service_password
        prof = profile.Profile()
        prof.set_region(profile.Profile.ALL, region)
        conn = connection.Connection(profile=prof, auth_url=auth_url,
                                     project_name=project_name,
                                     username=username, password=password,
                                     user_domain_name=user_domain_name,
                                     project_domain_name=project_domain_name)
        return conn.compute.reset_server_state(server, state)
