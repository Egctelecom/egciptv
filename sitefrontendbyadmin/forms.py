from django import forms

from sitefrontendbyadmin.models import MenuCategory,MenuParentCategory,MenuSubParentCategory,serviceandfeature,Specialoffersdoc,Slider

status = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('delete', 'delete')
    )
class MenuParentCategoryForm(forms.ModelForm):
    service_parent_category_name = forms.CharField(help_text='Enter Parent Category Name', max_length=255)
    status = forms.CharField(widget=forms.Select(choices=status), initial='active')

    class Meta:
        model = MenuParentCategory
        fields = '__all__'
        
class MenuSubParentCategoryForm(forms.ModelForm):
    service_sub_parent_category_name = forms.CharField(help_text='Enter Sub Parent Category Name', max_length=255)
    status = forms.CharField(widget=forms.Select(choices=status), initial='active')

    class Meta:
        model = MenuSubParentCategory
        fields = '__all__'
        
class MenuCategoryForm(forms.ModelForm):
    status = forms.CharField(widget=forms.Select(choices=status), initial='active')

    class Meta:
        model = MenuCategory
        fields = '__all__'


class ServicefeaturesForm(forms.ModelForm):
    details = forms.CharField(help_text='Enter Details', max_length=20000)
    status = forms.CharField(widget=forms.Select(choices=status), initial='active')
    service_feature_logo = forms.FileField()
    
    class Meta:
        model = serviceandfeature
        fields = '__all__'


class SpecialOffersDocForm(forms.ModelForm):
    special_offers_doc_name = forms.CharField(help_text='Enter Name', max_length=255)
    status = forms.CharField(widget=forms.Select(choices=status), initial='active')
    special_offers_doc = forms.FileField()
    
    class Meta:
        model = Specialoffersdoc
        fields = '__all__'

class SliderForm(forms.ModelForm):
      slider_name = forms.CharField(help_text='Enter Slider Name', max_length=255)
      details = forms.CharField(help_text='Enter Slider Name', max_length=8000)
      url = forms.CharField(help_text='Enter Slider Url', max_length=255)
      image = forms.FileField()
      status = forms.CharField(widget=forms.Select(choices=status), initial='active')
    
      class Meta:
             model = Slider
             fields = '__all__'