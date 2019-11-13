from django.db import models
from crmadmin.models import ManageServicesPriceCategory,ManageServicePrice
from adminsideserviceprovider.models import ServiceProviderPlan,Hardware
from adminsidecustomer.models import Province ,City

status = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('delete', 'delete')
    )

class MenuParentCategory(models.Model):
    id = models.AutoField(primary_key=True)
    service_parent_category_name = models.CharField(help_text='Enter Parent Service Name',max_length=255)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
class MenuSubParentCategory(models.Model):
    id = models.AutoField(primary_key=True)
    service_parent_category= models.ForeignKey(MenuParentCategory, on_delete=models.CASCADE)
    service_sub_parent_category_name = models.CharField(help_text='Enter Sub Parent Service Name',max_length=255)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
    
class MenuCategory(models.Model):
    id = models.AutoField(primary_key=True)
    service_category = models.ForeignKey(ManageServicesPriceCategory, on_delete=models.CASCADE)
    service_parent_category = models.ForeignKey(MenuParentCategory, on_delete=models.CASCADE)
    service_sub_parent_category_name = models.ForeignKey(MenuSubParentCategory, on_delete=models.CASCADE)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

#=========================================== Special offers Add ========================================================

class SpecialOffers(models.Model):
    id = models.AutoField(primary_key=True)
    details = models.TextField(help_text='Enter Details Name', blank=True)
    features = models.TextField(help_text='Enter Features',blank=True)
    actual_price = models.CharField(help_text='Enter Price', max_length=255, blank=True)
    offers_price = models.CharField(help_text='Enter Price', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id


class SpecialOffersPlans(models.Model):
    id = models.AutoField(primary_key=True)
    special_offers = models.ForeignKey(SpecialOffers, on_delete=models.CASCADE)
    service_price = models.ForeignKey(ManageServicePrice, on_delete=models.CASCADE)
    actual_price = models.CharField(help_text='Enter Price', max_length=255, blank=True)
    offers_price = models.CharField(help_text='Enter Price', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id


class SpecialOffersPlanswithHardwareRates(models.Model):
    id = models.AutoField(primary_key=True)
    special_offers = models.ForeignKey(SpecialOffers, on_delete=models.CASCADE)
    service_price = models.ForeignKey(ManageServicePrice, on_delete=models.CASCADE)
    service_plan = models.ForeignKey(ServiceProviderPlan, on_delete=models.CASCADE)
    hw = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    hw_qty = models.CharField(help_text='Enter Service Provider Plan Quantity', max_length=255)
    device_buy = models.CharField(help_text='Enter Device Buy', max_length=255, blank=True)
    device_rental = models.CharField(help_text='Enter Device Rental', max_length=255, blank=True)
    montly_rent = models.CharField(help_text='Enter Montly rent', max_length=255, blank=True)
    offer_price = models.CharField(help_text='Enter Offer Price', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id
    


class SpecialOffersPlansHardWare(models.Model):
    id = models.AutoField(primary_key=True)
    special_offers = models.ForeignKey(SpecialOffers, on_delete=models.CASCADE)
    service_price = models.ForeignKey(ManageServicePrice, on_delete=models.CASCADE)
    actual_price = models.CharField(help_text='Enter Price', max_length=255, blank=True)
    offers_price = models.CharField(help_text='Enter Price', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id

# Special Offers menu

class SpecialoffersParentCategory(models.Model):
    id = models.AutoField(primary_key=True)
    special_offers_parent_category_name = models.CharField(help_text='Enter Parent Service Name', max_length=255)
    desc = models.TextField(help_text='Enter Sub Parent Special Offers Description', blank=True)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id


class SpecialoffersSubParentCategory(models.Model):
    id = models.AutoField(primary_key=True)
    special_offers_parent_category = models.ForeignKey(SpecialoffersParentCategory, on_delete=models.CASCADE)
    special_offers_sub_parent_category_name = models.CharField(help_text='Enter Sub Parent Special Offers Name', max_length=255)
    desc = models.TextField(help_text='Enter Sub Parent Special Offers Description', blank=True)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id


class SpecialoffersUnderCategory(models.Model):
    id = models.AutoField(primary_key=True)
    special_offers = models.ForeignKey(SpecialOffers, on_delete=models.CASCADE)
    special_offers_parent_category = models.ForeignKey(SpecialoffersParentCategory, on_delete=models.CASCADE)
    special_offers_sub_parent_category = models.ForeignKey(SpecialoffersSubParentCategory, on_delete=models.CASCADE)
    special_offers_combo_name = models.CharField(help_text='Enter Special Offers Combo Name', max_length=255, blank=True)
    special_offers_type_name = models.CharField(help_text='Enter Special Offers Type Name', max_length=255, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    telecom_name = models.CharField(help_text='Enter Telecom Name', max_length=255, blank=True)
    telecom_logo = models.FileField(upload_to='static/telecom_logo/',blank=True)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id
    
class Specialoffersdoc(models.Model):
    id = models.AutoField(primary_key=True)
    special_offers = models.ForeignKey(SpecialOffers, on_delete=models.CASCADE)
    special_offers_doc_name = models.CharField(help_text='Enter Special Offers DOC Name', max_length=255,blank=True)
    special_offers_doc = models.FileField(upload_to='static/special_offers_doc/', blank=True)
    status = models.CharField(help_text='Enter Status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
#=========================================== Special offers End ========================================================


class serviceandfeature(models.Model):
    id = models.AutoField(primary_key=True)
    service_category = models.ForeignKey(ManageServicesPriceCategory, on_delete=models.CASCADE)
    service_parent_category = models.ForeignKey(MenuParentCategory, on_delete=models.CASCADE)
    service_sub_parent_category_name = models.ForeignKey(MenuSubParentCategory, on_delete=models.CASCADE)
    details=models.TextField(help_text='Enter Details Name',max_length=20000)
    service_feature_logo = models.FileField(upload_to='static/service_feature_logo/', blank=True)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id

#=========================================== Slider End ================================================================

class Slider(models.Model):
        id = models.AutoField(primary_key=True)
        slider_name = models.CharField(help_text='Enter Details Name',max_length=255)
        details = models.TextField(help_text='Enter Details Name',blank=True)
        image = models.FileField(upload_to='static/slider_image/', blank=True)
        url = models.CharField(help_text='Enter URL', max_length=255)
        status = models.CharField(help_text='Enter Status', choices=status, default='active', max_length=15)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
    
        def __str__(self):
            return self.id

#=========================================== Network Status ================================================================

class Network_status(models.Model):
    id = models.AutoField(primary_key=True)
    questions = models.TextField(help_text='Enter Details Name', blank=True)
    answers = models.TextField(help_text='Enter Details Name', blank=True)
    docs = models.FileField(upload_to='static/network_status_doc/', null=True)
    link = models.CharField(help_text='Enter URL', max_length=255)
    status = models.CharField(help_text='Enter Status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id


# =========================================== FAQs ================================================================

class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    questions = models.TextField(help_text='Enter Details Name',blank=True)
    answers = models.TextField(help_text='Enter Details Name', blank=True)
    docs = models.FileField(upload_to='static/faq_doc/', null=True)
    link = models.CharField(help_text='Enter URL', max_length=255)
    status = models.CharField(help_text='Enter Status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id

# =========================================== Follow Us ================================================================

class Followus(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField(help_text='Enter Details Name', blank=True)
    # image = models.FileField(upload_to='static/follow_us_icon/', null=True)
    fa_fa_icon = models.TextField(help_text='Enter fa fa icon', blank=True)
    status = models.CharField(help_text='Enter Status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id


#======================================== Upload Logo Area ==============================================


class WebLogo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='static/web_logo/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id



class BackgroundImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='static/bg_image/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id