from django import forms
from rateareacode.models import Ratewithareacode
status = (
        ('True', 'True'),
        ('False', 'False'),
)

class RatewithareacodeForm(forms.ModelForm):
    area_code = forms.CharField(help_text='Enter status', max_length=255)
    rate = forms.FloatField(help_text='Enter rate')
    status = forms.CharField(widget=forms.Select(choices=status), initial='True')

   
    class Meta:
	    model = Ratewithareacode
	    fields = '__all__'
