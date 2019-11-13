from django.db import models
from django.contrib.auth.models import User


class ContractSheet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title1 = models.TextField(help_text='Enter Title 1',blank=True)
    title2 = models.TextField(help_text='Enter Title 2',blank=True)
    title3 = models.TextField(help_text='Enter Title 3',blank=True)
    title4 = models.TextField(help_text='Enter Title 4',blank=True)
    title5 = models.TextField(help_text='Enter Title 5',blank=True)
    title6 = models.TextField(help_text='Enter Title 6',blank=True)
    title7 = models.TextField(help_text='Enter Title 7',blank=True)
    title8 = models.TextField(help_text='Enter Title 8',blank=True)
    title9 = models.TextField(help_text='Enter Title 9',blank=True)
    title10 = models.TextField(help_text='Enter Title 10',blank=True)
    title11 = models.TextField(help_text='Enter Title 11',blank=True)
    title12 = models.TextField(help_text='Enter Title 12',blank=True)
    title13 = models.TextField(help_text='Enter Title 13',blank=True)
    title14 = models.TextField(help_text='Enter Title 14',blank=True)
    title15 = models.TextField(help_text='Enter Title 15',blank=True)
    title16 = models.TextField(help_text='Enter Title 16',blank=True)
    title17 = models.TextField(help_text='Enter Title 17',blank=True)
    title18 = models.TextField(help_text='Enter Title 18',blank=True)
    title19 = models.TextField(help_text='Enter Title 19',blank=True)
    title20 = models.TextField(help_text='Enter Title 20',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
	