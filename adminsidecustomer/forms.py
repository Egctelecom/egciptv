from django import forms
from adminsidecustomer.models import Customer, CutomerAttachmentMap,Sales_tax
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap,ContractbasedHardwarewithMAC
from adminnumberprovider.models import NumberMNPtoCustomer


zone = (
        ('commercial', 'commercial'),
        ('residential', 'residential'),

    )

display_name = (
            ('user_name', 'user_name'),
            ('company_name', 'company_name'),
            )

prefferd_language = (
            ('english', 'english'),
            ('french', 'french'),
            )
priority = (
        ('low', 'L'),
        ('medium', 'M'),
        ('high', 'H'),

    )
category = (
        ('user', 'U'),
        ('administrator', 'A'),

    )


class Customerform(forms.ModelForm):
    account_id = forms.CharField(help_text='Enter asset', max_length=255)
    status = forms.CharField(help_text='Enter status', max_length=255)
    first_name = forms.CharField(help_text='Enter First Name', max_length=255)
    first_name_gsr = forms.CharField(help_text='Enter First Name GSR', max_length=255,required=False)
    last_name = forms.CharField(help_text='Enter Last Name', max_length=255)
    last_name_gsr = forms.CharField(help_text='Enter last Name GSR', max_length=255,required=False)
    company_name = forms.CharField(help_text='Enter Company Name', max_length=255, required=False)
    company_name_gsr = forms.CharField(help_text='Enter Comapny Name GSR', max_length=255,required=False)
    email_address = forms.CharField(help_text='Enter Email Address', max_length=255)
    phone = forms.IntegerField(help_text='Enter Phone')
    portal_password = forms.CharField(help_text='Enter Portal Password', max_length=255)
    other_phone = forms.IntegerField(help_text='Enter Other Phone')
    dob = forms.CharField(help_text='Enter Date Of Birth', max_length=255)
    display_name = forms.CharField(widget=forms.Select(choices=display_name), initial='user_name')
    prefferd_language = forms.CharField(widget=forms.Select(choices=prefferd_language), initial='english')
    zone = forms.CharField(widget=forms.Select(choices=zone), initial='commercial')

    class Meta:
        model = Customer
        fields = ('account_id', 'status', 'first_name','first_name_gsr','portal_password','last_name','last_name_gsr','company_name','company_name_gsr','email_address','phone','other_phone','dob','display_name','zone','prefferd_language')

class CutomerAttachmentform(forms.ModelForm):
    file_name = forms.CharField(help_text='Enter status', max_length=255)
    filedata = forms.FileField()
    file_type = forms.CharField(help_text='Enter file type', max_length=255)

    class Meta:
        model = CutomerAttachmentMap
        fields = '__all__'

class CustomerTicketsform(forms.ModelForm):

    subject = forms.CharField(help_text='Enter Subjects', max_length=255)
    threads = forms.CharField(help_text='Enter Threads', max_length=255)
    category = forms.CharField(widget=forms.Select(choices=zone), initial='U')
    priority = forms.CharField(widget=forms.Select(choices=zone), initial='L')

    class Meta:
        model = CustomerTicketsCategoriesMap
        fields = '__all__'

class ContractbasedHardwareform(forms.ModelForm):

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
        model = ContractbasedHardwarewithMAC
        fields = '__all__'


class NumberMNPtoCustomerform(forms.ModelForm):
    number = forms.IntegerField(help_text='Enter number')
    approve_upload_data = forms.FileField()

    class Meta:
        model = NumberMNPtoCustomer
        fields = '__all__'


#--------------------------------------------------- Sales tax --------------------------------------------------------------------

class SalesTaxform(forms.ModelForm):
    tax_name = forms.CharField(help_text='Enter Service Name', max_length=255)
    abbreviation = forms.CharField(help_text='Enter Service Name', max_length=255)
    description = forms.CharField(help_text='Enter Service Name', max_length=255)
    tax_number = forms.IntegerField()
    is_tax_number_show = forms.CharField(help_text='Enter Service Name', max_length=255)
    is_fedral_tax = forms.CharField(help_text='Enter Service Name', max_length=255)
    is_provisional_tax = forms.CharField(help_text='Enter Service Name', max_length=255)
    tax_rate = forms.FloatField()

    class Meta:
        model = Sales_tax
        fields = "__all__"