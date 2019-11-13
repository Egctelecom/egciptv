from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from  settingcontractsheet.models import ContractSheet
from  adminsidecustomer.models import CustomerUserMap

def my_check(user):
    return user.is_superuser == True

#============================================================================== Country ==========================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def update_contract_sheet(request,pk):
    
    AuthUserID = CustomerUserMap.objects.values('user_id').filter(customer_id=pk)
    

    data = ContractSheet.objects.values('user_id',
                                        'title1',
                                        'title2',
                                        'title3',
                                        'title4',
                                        'title5',
                                        'title6',
                                        'title7',
                                        'title8',
                                        'title9',
                                        'title10',
                                        'title11',
                                        'title12',
                                        'title13',
                                        'title14',
                                        'title15',
                                        'title16',
                                        'title17').filter(user_id=AuthUserID[0]['user_id'])
    return render(request, 'admin/settingcontractsheet/index.html',{'data':data,'pk':pk})

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def save_contractsheet(request):
    if request.is_ajax():
        title1 =  request.POST['title1']
        title2 =  request.POST['title2']
        title3 =  request.POST['title3']
        title4 =  request.POST['title4']
        title5 =  request.POST['title5']
        title6 =  request.POST['title6']
        title7 =  request.POST['title7']
        title8 =  request.POST['title8']
        title9 =  request.POST['title9']
        title10 =  request.POST['title10']
        title11 =  request.POST['title11']
        title12 =  request.POST['title12']
        title13 =  request.POST['title13']
        title14 =  request.POST['title14']
        title15 =  request.POST['title15']
        title16 =  request.POST['title16']
        title17 =  request.POST['title17']
        customer_id =  request.POST['user_id']
        
        
        user = CustomerUserMap.objects.values('user_id').filter(customer_id=customer_id)


        if ContractSheet.objects.exists():
            sheet_id = ContractSheet.objects.values('id')
            obj = ContractSheet.objects.get(pk=sheet_id[0]['id'])
            obj.user_id=user[0]['user_id']
            obj.title1=title1
            obj.title2=title2
            obj.title3=title3
            obj.title4=title4
            obj.title5=title5
            obj.title6=title6
            obj.title7=title7
            obj.title8=title8
            obj.title9=title9
            obj.title10=title10
            obj.title11=title11
            obj.title12=title12
            obj.title13=title13
            obj.title14=title14
            obj.title15=title15
            obj.title16=title16
            obj.title17=title17
            obj.save()
            
            response_data = {}
            response_data['title1'] = title1
            response_data['title2'] = title2
            response_data['title3'] = title3
            response_data['title4'] = title4
            response_data['title5'] = title5
            response_data['title6'] = title6
            response_data['title7'] = title7
            response_data['title8'] = title8
            response_data['title9'] = title9
            response_data['title10'] = title10
            response_data['title11'] = title11
            response_data['title12'] = title12
            response_data['title13'] = title13
            response_data['title14'] = title14
            response_data['title15'] = title15
            response_data['title16'] = title16
            response_data['title17'] = title17

            return JsonResponse(response_data, safe=False)
        else:
            ContractSheet.objects.create(user_id=user[0]['user_id'],
                                         title1=title1,
                                         title2=title2,
                                         title3=title3,
                                         title4=title4,
                                         title5=title5,
                                         title6=title6,
                                         title7=title7,
                                         title8=title8,
                                         title9=title9,
                                         title10=title10,
                                         title11=title11,
                                         title12=title12,
                                         title13=title13,
                                         title14=title14,
                                         title15=title15,
                                         title16=title16,
                                         title17=title17
                                         )
            response_data={}
            response_data['title1']=title1
            response_data['title2']=title2
            response_data['title3']=title3
            response_data['title4']=title4
            response_data['title5']=title5
            response_data['title6']=title6
            response_data['title7']=title7
            response_data['title8']=title8
            response_data['title9']=title9
            response_data['title10']=title10
            response_data['title11']=title11
            response_data['title12']=title12
            response_data['title13']=title13
            response_data['title14']=title14
            response_data['title15']=title15
            response_data['title16']=title16
            response_data['title17']=title17
            
            return JsonResponse(response_data,safe=False)
        
        
        
        



