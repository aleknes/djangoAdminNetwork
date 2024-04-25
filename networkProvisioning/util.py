from ipaddress import IPv4Network

from django.db.models import Q
from jinja2 import Template
import pprint

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
    def build_configuration_alternate(router_obj):
        """Testing som changes to the build_configuration method"""
        if router_obj.template:
            from networkProvisioning.models import Link, NetworkConfiguration
            template = router_obj.template.template_file.file.read().decode('utf-8')

            #Get links where I am side A. Must fix IP addresses problem
            router_obj.links = router_obj.getLinksLocal()

            print (f'Links: {router_obj.links}')
            links_data = []

            links = router_obj.getLinksLocal()
            print(links)

            for link in router_obj.getLinksLocal():
                # Convert link object to a dictionary
                link_dict = {
                    field.name: getattr(link, field.name)
                    for field in link._meta.fields
                }
                links_data.append(link_dict)  

            router_obj.links = links_data
            router_obj.location = router_obj.site.name
            router_obj.ntp_servers = router_obj.base_config.ntp_servers
            router_obj.syslog_servers = router_obj.base_config.syslog_servers

            for other in router_obj.base_config.other_json:
                setattr(router_obj, other, router_obj.base_config.other_json[other])

            pprint.pprint(router_obj.__dict__)

            config = Template(template).render(router_obj.__dict__)
            config = Util.populateSecrets(config)
            return config
        
    @staticmethod
    def populateSecrets(config):
        #Mock function to populate secrets
        if True == True:
            return config

    
    @staticmethod
    def update_available_interfaces(obj, action):
        
        for side in ['side_a', 'side_b']:
            print(f'Updating {side} interfaces')
            router, intf = getattr(obj, side), getattr(obj, f'{side}_intf')
            print(f'Router: {router}')
            print("available interfaces: ", router.available_interfaces)
            print(f'Interface: {intf}')
            from networkProvisioning.models import Link
            existing_intf = getattr(
                Link.objects.filter(id=obj.id).first(),
                f'{side}_intf',
                None
            )
            print(f'Existing Interface: {existing_intf}')
            if action == 'remove':
        
                if intf in router.available_interfaces:
                    if existing_intf:
                        if existing_intf not in router.available_interfaces:
                            print(f'Adding {existing_intf} back to available interfaces')
                            router.available_interfaces.append(existing_intf)
                    router.available_interfaces.remove(intf)
            else:
                print(f'Adding {intf} to available interfaces')
                router.available_interfaces.append(intf)

            router.available_interfaces.sort()
            router.save()
