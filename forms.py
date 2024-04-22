from django import forms

from networkProvisioning.models import Link


class LinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # override side a and b interfaces. replace with router instances available interfaces

        def set_interface_choices(_side):
            router, intf = getattr(self.instance, _side), getattr(self.instance, f'{_side}_intf')
            intf_numbers = [(i, i) for i in router.available_interfaces]
            intf_numbers += [(intf, intf)]

            intf_prefixes = [(i, i) for i in router.serial_number.device_model.operating_system.interface_prefixes]

            if hasattr(self.instance, _side):
                self.fields[f'{_side}_intf'] = forms.ChoiceField(choices=intf_numbers)
                self.fields[f'{_side}_prefix'] = forms.ChoiceField(choices=intf_prefixes)

        if hasattr(self.instance, 'side_a') and hasattr(self.instance, 'side_b'):
            for side in ['side_a', 'side_b']:
                set_interface_choices(side)
        else:
            for side in ['side_a', 'side_b']:
                self.fields[f'{side}_intf'].widget.attrs['hidden'] = True
                self.fields[f'{side}_prefix'].widget.attrs['hidden'] = True

    class Meta:
        model = Link
        fields = '__all__'
