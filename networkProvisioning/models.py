from django.db import models

# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=255)
    planned_install_date = models.DateField(null=True, blank=True)
    installation_status = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class SerialNumber(models.Model):
    number = models.CharField(max_length=255, unique=True)
    part_number = models.CharField(max_length=255)

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

class Switch(GenericDevice):
    class Meta:
        verbose_name_plural = 'Switches'
    mgmt_ip = models.GenericIPAddressField(unique=True)
