from django import forms
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderPlan, ServicePlanWithHardware, Hardware,TicketsCategories,TicketsCategoryWithServiceProvider


hw_status=(
    ('Buy', 'Buy'),
    ('Rental', 'Rental'),
    ('MonthlyRent', 'MonthlyRent')
)
status = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('delete', 'delete')
    )

class ServiceProviderform(forms.ModelForm):

    service_provider_name = forms.CharField(help_text='Enter Service Provider Name', max_length=255)

    class Meta:
        model = ServiceProvider
        fields = ('id','service_provider_name')




class ServiceProviderPlanform(forms.ModelForm):

    # service_provider_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(help_text='Enter Service Provider Plan Name', max_length=255)
    retail = forms.CharField(help_text='Enter Service Provider Plan Retail Value', max_length=255)
    actual = forms.CharField(help_text='Enter Service Provider Plan Actual Value', max_length=255)
    qty = forms.CharField(help_text='Enter Service Provider Plan Quantity ', max_length=255)
    status = forms.CharField(widget=forms.Select(choices=status), initial='active')

    class Meta:
        model = ServiceProviderPlan
        fields = '__all__'




class ServicePlanWithHardwareform(forms.ModelForm):

    # service_provider_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    hw_qty = forms.CharField(help_text='Enter Service Provider Plan Quantity ', max_length=255)
    hw_status = forms.CharField(widget=forms.Select(choices=hw_status), initial='Buy')


    class Meta:
        model = ServicePlanWithHardware
        fields = '__all__'


class Hardwareform(forms.ModelForm):

    # service_provider_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    hw_title = forms.CharField(help_text='Enter H/W name ', max_length=255)
    type = forms.CharField(max_length=255,required=False)
    model = forms.CharField(max_length=255,required=False)
    mac = forms.CharField(max_length=255,required=False)
    sn = forms.CharField(max_length=255,required=False)
    ver = forms.CharField(max_length=255,required=False)
    usrn = forms.CharField(max_length=255,required=False)
    passu = forms.CharField(max_length=255,required=False)
    adusr = forms.CharField(max_length=255,required=False)
    adpass = forms.CharField(max_length=255,required=False)
    dslusr = forms.CharField(max_length=255,required=False)
    dslpass = forms.CharField(max_length=255,required=False)
    date_start = forms.CharField(max_length=255,required=False)
    date_end = forms.CharField(max_length=255,required=False)
    still_in_service = forms.CharField(max_length=255,required=False)
    device_buy = forms.CharField(max_length=255,required=False)
    device_rental = forms.CharField(max_length=255,required=False)
    montly_rent = forms.CharField(max_length=255,required=False)


    class Meta:
        model = Hardware
        fields = '__all__'


class Ticketform(forms.ModelForm):

    category_title =forms.CharField(max_length=255,required=False)

    class Meta:
        model = TicketsCategories
        fields = '__all__'


class TicketWithServiceProviderform(forms.ModelForm):


    class Meta:
        model = TicketsCategoryWithServiceProvider
        fields = '__all__'
