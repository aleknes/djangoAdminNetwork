from django import forms

from networkProvisioning.models import Router, Link


class LinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # override side a and b interfaces. replace with router instances available interfaces

        def set_interface_choices(side):
            router, intf = getattr(self.instance, side), getattr(self.instance, f'{side}_intf')
            choices = [ (i,i) for i in router.available_interfaces ]
            choices += [(intf, intf)]
            if hasattr(self.instance, side):
                self.fields[f'{side}_intf'] = forms.ChoiceField(choices=choices)

        if hasattr(self.instance, 'side_a') and hasattr(self.instance, 'side_b'):
            for side in ['side_a', 'side_b']:
                set_interface_choices(side)
        else:
            self.fields['side_a_intf'].widget.attrs['readonly'] = True
            self.fields['side_b_intf'].widget.attrs['readonly'] = True

    class Meta:
        model = Link
        fields = '__all__'
