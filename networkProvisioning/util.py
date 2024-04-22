from ipaddress import IPv4Network

from django.db.models import Q
from jinja2 import Template


class Util:
    @staticmethod
    def build_configuration(router_obj):
        if router_obj.template:
            from networkProvisioning.models import Link
            template = router_obj.template.template_file.file.read().decode('utf-8')
            # get links that belongs to me
            link_filter = Q(side_a=router_obj) | Q(side_b=router_obj)
            # just add link as property to router obj and use it as context
            router_obj.links = Link.objects.filter(link_filter)
            # generate a list of hosts from the link subnet
            for link in router_obj.links:
                if link.subnet:
                    subnet = IPv4Network(link.subnet, strict=False)
                    link.subnet = list(subnet.hosts())
                    link.netmask = subnet.netmask

            return Template(template).render(router_obj.__dict__)

    @staticmethod
    def update_available_interfaces(obj, action):
        for side in ['side_a', 'side_b']:
            router, intf = getattr(obj, side), getattr(obj, f'{side}_intf')
            from networkProvisioning.models import Link
            existing_intf = getattr(
                Link.objects.filter(id=obj.id).first(),
                f'{side}_intf',
                None
            )
            if action == 'remove':
                if intf in router.available_interfaces:
                    if existing_intf:
                        if existing_intf not in router.available_interfaces:
                            router.available_interfaces.append(existing_intf)
                    router.available_interfaces.remove(intf)
            else:
                router.available_interfaces.append(intf)

            router.available_interfaces.sort()
            router.save()
