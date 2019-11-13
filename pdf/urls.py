from django.conf.urls import url

from pdf.views import GeneratePdf,GeneratePdffrench

urlpatterns = [
        url(r'^$',  GeneratePdf.as_view(),name='pdf'),
        url(r'^french/$',  GeneratePdffrench.as_view(),name='pdf_french'),
]
