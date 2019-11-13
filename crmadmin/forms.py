from django import forms

from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice, Services,UserImage
from adminsideserviceprovider.models import ManageServicePricedoc
from sitefrontendbyadmin.models import SpecialOffers,SpecialoffersParentCategory,SpecialoffersSubParentCategory,SpecialoffersUnderCategory

status = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('delete', 'delete')
    )

class ManageServicesPriceCategoryForm(forms.ModelForm):
    service_category_name = forms.CharField(help_text='Enter Category Name', max_length=255)
    status = forms.CharField(widget=forms.Select(choices=status), initial='Active')

    class Meta:
        model = ManageServicesPriceCategory
        fields = ('service_category_name', 'status')


class ManageServicesPriceForm(forms.ModelForm):
    service_name = forms.CharField(help_text='Enter Service Name', max_length=255)
    service_price = forms.FloatField(help_text='Enter Service Price')
    service_desc = forms.CharField(max_length=15000,widget=forms.Textarea)
    status = forms.CharField(widget=forms.Select(choices=status), initial='Active')
    special_offer = forms.CharField(help_text='Enter Special Offer', max_length=255)

    class Meta:
        model = ManageServicePrice
        fields = "__all__"
        
class ManageServicePricedocForm(forms.ModelForm):
    service_price_doc_name = forms.CharField(help_text='Enter Service Price Document Name', max_length=255)
    status = forms.CharField(widget=forms.Select(choices=status), initial='active')
    service_price_doc = forms.FileField()
  

    class Meta:
        model = ManageServicePricedoc
        fields = "__all__"

#--------------------------------------------------- Service ---------------------------------------------------------------------------

class Serviceform(forms.ModelForm):
    title = forms.CharField(help_text='Enter Service Name', max_length=255)
    price = forms.FloatField()

    class Meta:
        model = Services
        fields = ('title', 'price')

#--------------------------------------------------- Umage -----------------------------------------------------------------------------

class UserImageform(forms.ModelForm):
    avatardata = forms.FileField()
    
    class Meta:
        model = UserImage
        fields = "__all__"

# --------------------------------------------------- Special Offers --------------------------------------------------------------------

class SpecialOffersform(forms.ModelForm):
    
    details = forms.CharField(help_text='Enter Details Name')
    features = forms.CharField(help_text='Enter Features')
    actual_price = forms.CharField(help_text='Enter Price', max_length=255)
    offers_price = forms.CharField(help_text='Enter Price', max_length=255)
    
    class Meta:
        model = SpecialOffers
        fields ="__all__"



class SpecialoffersParentCategoryForm(forms.ModelForm):
    special_offers_parent_category_name = forms.CharField(help_text='Enter Parent Category Name', max_length=255)
    desc = forms.CharField(help_text='Enter Desc')
    status = forms.CharField(widget=forms.Select(choices=status), initial='Active')

    
    class Meta:
        model = SpecialoffersParentCategory
        fields = '__all__'


class SpecialoffersSubParentCategoryForm(forms.ModelForm):
    special_offers_sub_parent_category_name = forms.CharField(help_text='Enter Sub Parent Category Name', max_length=255)
    desc = forms.CharField(help_text='Enter Desc')
    status = forms.CharField(widget=forms.Select(choices=status), initial='Active')

    
    class Meta:
        model = SpecialoffersSubParentCategory
        fields = '__all__'


class SpecialoffersUnderCategoryForm(forms.ModelForm):
    special_offers_combo_name = forms.CharField(help_text='Enter Special Offers Combo Name', max_length=255)
    special_offers_type_name = forms.CharField(help_text='Enter Special Offers Type Name', max_length=255)
    telecom_name = forms.CharField(help_text='Enter Telecom Name', max_length=255)
    telecom_logo = forms.FileField()
    status = forms.CharField(widget=forms.Select(choices=status), initial='Active')
    
    class Meta:
        model = SpecialoffersUnderCategory
        fields = '__all__'