import os

from django.core.files.storage import FileSystemStorage
from django.db import models

from networkProvisioning.util import Util

from ipaddress import IPv4Network


# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=255)
    planned_install_date = models.DateField(null=True, blank=True)
    installation_status = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class NetworkConfiguration(models.Model):
    name = models.CharField(max_length=255)
    syslog_servers = models.JSONField(default=list, null=True, blank=True)
    ntp_servers = models.JSONField(default=list, null=True, blank=True)
    other_json = models.JSONField(default=dict, null=True, blank=True)


    def __str__(self):
        return self.name

class SerialNumber(models.Model):
    number = models.CharField(max_length=255, unique=True)
    device_model = models.ForeignKey('DeviceModel', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.number


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, **kwargs):
        if self.exists(name):
            os.remove(os.path.join('', name))
        return name


class Template(models.Model):
    name = models.CharField(max_length=255)
    template_file = models.FileField(upload_to='networkProvisioning/configuration_templates/', storage=OverwriteStorage())

    def __str__(self):
        return self.name


class GenericDevice(models.Model):
    hostname = models.CharField(max_length=255)
    domain = models.CharField(max_length=20, blank=True, null=True)
    serial_number = models.OneToOneField(SerialNumber, unique=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True, help_text='Select Template to view configuration')
    configuration_url = models.URLField(null=True, blank=True,
                                        help_text='WIP: Should be available on an UUID URL when finished')
    provisioned = models.BooleanField(null=True, blank=True, help_text='Automatically set based on ZTP status')
    base_config = models.ForeignKey(NetworkConfiguration, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.hostname


class Router(GenericDevice):
    loopback_ip = models.GenericIPAddressField(unique=True, help_text='Implicit /32')
    available_interfaces = models.JSONField(help_text='Automatically generated/updated when saving router or link')

    def getLinksLocal(self):
        #Returns all links where the side_a is the local router
        from networkProvisioning.models import Link
        links = Link.objects.filter(side_a=self) | Link.objects.filter(side_b=self)
        return_links = []
        print(f"Links getlinkslocal : {links}")
        if links:
            for link in links:
                if link.side_a == self:
                    return_links.append(link)
                else:
                    return_links.append(link.get_swapped_link())
        return return_links


    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.available_interfaces:
            self.available_interfaces = self.serial_number.device_model.interface_numbers

        Util.build_configuration(self)
        super().save(force_insert, force_update, using, update_fields)

#AL: Added this for extra functionality, but ended up using hostname as metadata for logc in jinja templates. Can probably be removed.
class TransportRouter(Router):
    class Meta:
        verbose_name = 'Transport Router'

class CERouter(Router):
    class Meta:
        verbose_name = 'CE Router'

class Switch(GenericDevice):
    class Meta:
        verbose_name_plural = 'Switches'

    mgmt_ip = models.GenericIPAddressField(unique=True)


class Link(models.Model):
    intf_help_text = 'Choose sides and then click "Save and continue editing" to see list of available choices'
    side_a = models.ForeignKey(Router, related_name='side_a', on_delete=models.CASCADE)
    side_a_prefix = models.CharField(max_length=255, help_text=intf_help_text, null=True, blank=True)
    side_a_intf = models.CharField(max_length=255, help_text=intf_help_text, blank=True, null=True)
    side_a_ipv4_address = models.GenericIPAddressField(null=True, blank=True, editable=True, help_text='Automatically genereated from subnet when saving')
    side_b = models.ForeignKey(Router, related_name='side_b', on_delete=models.CASCADE)
    side_b_prefix = models.CharField(max_length=255, help_text=intf_help_text, null=True, blank=True)
    side_b_intf = models.CharField(max_length=255, help_text=intf_help_text, blank=True, null=True)
    side_b_ipv4_address = models.GenericIPAddressField(null=True, blank=True, editable=True, help_text='Automatically genereated from subnet when saving')
    circuit_id = models.CharField(max_length=255, blank=True, null=True)
    subnet_mask = models.CharField(max_length=255, blank=True, null=True, editable=True, help_text='Automatically generated from subnet when saving')

    subnet = models.CharField(max_length=255, blank=True, null=True,
                              help_text='Automatically fetched from IPAM when saving')
    def get_swapped_link(self):
        swapped_link = Link(
            side_a=self.side_b,
            side_a_prefix=self.side_b_prefix,
            side_a_intf=self.side_b_intf,
            side_a_ipv4_address=self.side_b_ipv4_address,
            side_b=self.side_a,
            side_b_prefix=self.side_a_prefix,
            side_b_intf=self.side_a_intf,
            side_b_ipv4_address=self.side_a_ipv4_address,
            circuit_id=self.circuit_id,
            subnet=self.subnet,
            subnet_mask=self.subnet_mask
        )
        return swapped_link
    def __str__(self):
        return f'{self.side_a}:{self.side_a_intf} <-> {self.side_b}:{self.side_b_intf}'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        print (type(self.subnet))
        print("asdasdas")
        """
        if self.subnet:
             subnet = IPv4Network(self.subnet, strict=False)
             self.side_a_ipv4_address = list(subnet.hosts())[0]
             self.side_b_ipv4_address = list(subnet.hosts())[1]
             self.subnet_mask = subnet.netmask
             print("Subnet")

        """
        if self.subnet:
            print("hi   ")
            subnet = IPv4Network(self.subnet, strict=False)
            self.subnet_mask = subnet.netmask    

            ip_addresses = list(subnet.hosts())
            self.side_a_ipv4_address = str(ip_addresses[0])
            self.side_b_ipv4_address = str(ip_addresses[1])

        Util.update_available_interfaces(self, 'remove')
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        Util.update_available_interfaces(self, 'restore')
        super().delete(using, keep_parents)


class OperatingSystem(models.Model):
    name = models.CharField(max_length=255)
    interface_prefixes = models.JSONField()

    def __str__(self):
        return self.name


class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.DO_NOTHING, null=True, blank=True)
    hardware_url = models.URLField(null=True, blank=True)
    interface_numbers = models.JSONField()

    def __str__(self):
        return f'{self.part_number}'
