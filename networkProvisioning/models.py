from django.db import models

from networkProvisioning.util import Util


# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=255)
    planned_install_date = models.DateField(null=True, blank=True)
    installation_status = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class SerialNumber(models.Model):
    number = models.CharField(max_length=255, unique=True)
    device_model = models.ForeignKey('DeviceModel', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.number


class GenericDevice(models.Model):
    hostname = models.CharField(max_length=255)
    serial_number = models.OneToOneField(SerialNumber, unique=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    configuration_url = models.URLField(null=True, blank=True)
    provisioned = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.hostname


class Router(GenericDevice):
    loopback_ip = models.GenericIPAddressField(unique=True)
    available_interfaces = models.JSONField(help_text='Automatically generated from device model when saving')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.available_interfaces:
            self.available_interfaces = self.serial_number.device_model.interface_numbers

        super().save(force_insert, force_update, using, update_fields)

class Switch(GenericDevice):
    class Meta:
        verbose_name_plural = 'Switches'

    mgmt_ip = models.GenericIPAddressField(unique=True)

class Link(models.Model):
    intf_help_text = 'click Save and continue to see list of available interfaces'
    side_a = models.ForeignKey(Router, related_name='side_a', on_delete=models.CASCADE)
    side_a_intf = models.CharField(max_length=255, help_text=intf_help_text, blank=True, null=True)
    side_b = models.ForeignKey(Router, related_name='side_b', on_delete=models.CASCADE)
    side_b_intf = models.CharField(max_length=255, help_text=intf_help_text, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    subnet = models.GenericIPAddressField(blank=True, null=True, help_text='Automatically fetched from IPAM when saving')


    def __str__(self):
        return f'{self.side_a}:{self.side_a_intf} <-> {self.side_b}:{self.side_b_intf}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        Util.update_available_interfaces(self, 'remove')
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        Util.update_available_interfaces(self, 'restore')
        super().delete(using, keep_parents)

class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    hardware_url = models.URLField(null=True, blank=True)
    interface_numbers = models.JSONField()
    def __str__(self):
        return f'{self.part_number}'
