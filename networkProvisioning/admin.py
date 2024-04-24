from copy import deepcopy

from django.contrib import admin
from django.utils.html import format_html

import networkProvisioning.admin_actions
from forms import LinkForm
from networkProvisioning.models import Site, SerialNumber, Router, Switch, Link, DeviceModel, Template, OperatingSystem, \
    GenericDevice, NetworkConfiguration
from networkProvisioning.util import Util


# Register your models here.
@admin.register(SerialNumber)
class SerialNumberAdmin(admin.ModelAdmin):
    @staticmethod
    def assigned_to_device(obj):
        return GenericDevice.objects.filter(serial_number=obj).first()

    list_display = [
        'number',
        'device_model',
        'assigned_to_device'
    ]


class DeviceAdmin(admin.ModelAdmin):
    @staticmethod
    def configuration_preview(obj):
        return Util.build_configuration(obj)

    list_display = [
        'hostname',
        'site',
        'serial_number',
        'template',
        'provisioned'
    ]
    readonly_fields = [
        'provisioned',
    ]
    search_fields = [
        'hostname',
        'site__name',
        'serial_number__number',
    ]


@admin.register(Router)
class RouterAdmin(DeviceAdmin):
    list_display = deepcopy(DeviceAdmin.list_display)
    list_display.insert(1, 'loopback_ip')
    actions = [
        networkProvisioning.admin_actions.perform_some_action,
    ]
    readonly_fields = [
        'available_interfaces',
        'configuration_url',
        'configuration_preview',
    ]


@admin.register(Switch)
class SwitchAdmin(DeviceAdmin):
    list_display = deepcopy(DeviceAdmin.list_display)
    list_display.insert(1, 'mgmt_ip')


class DeviceAdminInline(admin.TabularInline):
    class Media:
        js = ['deviceactions.js']

    extra = 0
    can_delete = False

    @staticmethod
    def action(obj):
        return format_html('''
            <button type="button" onclick="getShowVersion(this);" class="btn btn-warning">Get Show Version</button>
        ''')

    readonly_fields = [
        'action',
        'provisioned',
    ]


class RouterAdminInline(DeviceAdminInline):
    model = Router
    fields = [
        'hostname',
        'serial_number',
        'loopback_ip',
        'action',
        'provisioned'
    ]


class SwitchAdminInline(DeviceAdminInline):
    model = Switch
    fields = [
        'hostname',
        'serial_number',
        'mgmt_ip',
        'action',
        'provisioned'
    ]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'planned_install_date',
        'installation_status',
    ]
    inlines = [
        RouterAdminInline,
        SwitchAdminInline,
    ]

@admin.register(NetworkConfiguratio n)
class NetworkConfigurationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'syslog_servers',
        'ntp_servers',
    ]



@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    @staticmethod
    def _side_a_intf(obj):
        return f'{obj.side_a_prefix}{obj.side_a_intf}'

    @staticmethod
    def _side_b_intf(obj):
        return f'{obj.side_b_prefix}{obj.side_b_intf}'

    list_display = [
        'circuit_id',
        'subnet',
        'side_a',
        '_side_a_intf',
        'side_b',
        '_side_b_intf',
    ]

    form = LinkForm


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'part_number',
        'interface_numbers',
    ]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'template_file',
    ]


@admin.register(OperatingSystem)
class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
