from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import http.client
import json
import requests


def my_check(user):
	return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def cdr_details(request):
	if request.method == 'GET':
		headers = {
			'cache-control': "no-cache",
			'Postman-Token': "ac92ca24-3d5b-4d47-8fa6-a57b2fed168f"
		}
		payload = ""
		url2 = "https://cdr.teleapi.net/cdr/04-24-2017/04-26-2018?token=73ad3b26-88a2-4f59-90ae-9be6a256782d"
		response2 = requests.request("GET", url2, data=payload, headers=headers)
		data = response2.text
		date_gmt = []
		source = []
		destination = []
		callerid = []
		hangup_code = []
		sip_account = []
		orig_ip = []
		duration = []
		per_minute = []
		callcost = []
		type = []
		uuid = []
		data_array = data.split('\r\n')
		i = 0
		for i in range(len(data_array) - 1):
			if i > 0:
				row_data = data_array[i].split(',')
				date_gmt.append(row_data[0])
				source.append(row_data[1])
				destination.append(row_data[2])
				callerid.append(row_data[3])
				hangup_code.append(row_data[4])
				sip_account.append(row_data[5])
				orig_ip.append(row_data[6])
				duration.append(row_data[7])
				per_minute.append(row_data[8])
				callcost.append(row_data[9])
				type.append(row_data[10])
				uuid.append(row_data[11])
			i = i + 1


		return render(request, 'admin/cdr/index.html', {'date_gmt': date_gmt,
		                                                'source': source,
		                                                'destination': destination,
		                                                'callerid': callerid,
		                                                'hangup_code': hangup_code,
		                                                'sip_account': sip_account,
		                                                'orig_ip': orig_ip,
		                                                'duration': duration,
		                                                'per_minute': per_minute,
		                                                'callcost': callcost,
		                                                'type': type,
		                                                'uuid': uuid,
		                                                })


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def cdr_date_filter_details(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']
		headers = {
			'cache-control': "no-cache",
			'Postman-Token': "ac92ca24-3d5b-4d47-8fa6-a57b2fed168f"
		}
		payload = ""
		url2 = "https://cdr.teleapi.net/cdr/" + start_date + "/" + end_date + "?token=73ad3b26-88a2-4f59-90ae-9be6a256782d"
		response2 = requests.request("GET", url2, data=payload, headers=headers)
		data = response2.text
		date_gmt = []
		source = []
		destination = []
		callerid = []
		hangup_code = []
		sip_account = []
		orig_ip = []
		duration = []
		per_minute = []
		callcost = []
		type = []
		uuid = []
		data_array = data.split('\r\n')
		i = 0
		for i in range(len(data_array) - 1):
			if i > 0:
				row_data = data_array[i].split(',')
				date_gmt.append(row_data[0])
				source.append(row_data[1])
				destination.append(row_data[2])
				callerid.append(row_data[3])
				hangup_code.append(row_data[4])
				sip_account.append(row_data[5])
				orig_ip.append(row_data[6])
				duration.append(row_data[7])
				per_minute.append(row_data[8])
				callcost.append(row_data[9])
				type.append(row_data[10])
				uuid.append(row_data[11])
			i = i + 1
		return render(request, 'admin/cdr/index.html', {'date_gmt': date_gmt,
		                                                'source': source,
		                                                'destination': destination,
		                                                'callerid': callerid,
		                                                'hangup_code': hangup_code,
		                                                'sip_account': sip_account,
		                                                'orig_ip': orig_ip,
		                                                'duration': duration,
		                                                'per_minute': per_minute,
		                                                'callcost': callcost,
		                                                'type': type,
		                                                'uuid': uuid,
		                                                'start_date': start_date,
		                                                'end_date': end_date
		                                                })
