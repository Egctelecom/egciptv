from django import forms
from adminsidecustomer.models import Country,Province,City

class Setcountryform(forms.ModelForm):
    country_name = forms.CharField(help_text='Enter Country Name', max_length=255)

    class Meta:
        model = Country
        fields = '__all__'
        
class Setprovinceform(forms.ModelForm):
    province_name = forms.CharField(help_text='Enter Province Name', max_length=255)

    class Meta:
        model = Province
        fields = '__all__'
        
        
class Setcityform(forms.ModelForm):
    city_name = forms.CharField(help_text='Enter City Name', max_length=255)

    class Meta:
        model = City
        fields = '__all__'