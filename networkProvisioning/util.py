

class Util:
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