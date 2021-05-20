#!/usr/bin/env python

import requests
import platform
import os
import time, threading
import json
from datetime import datetime

vaccine_type = "COVAXIN" # or COVAXIN or COVISHIELD
min_age_limit = 45 # of 18
# district mapping : https://github.com/bhattbhavesh91/cowin-vaccination-slot-availability/blob/main/district_mapping.csv

def beep():
	if platform.system().startswith('CYGWIN_NT'):
		os.system('cygstart ./beep.mp3')
	else:
		print "Check if the Available slots are nearby your area !!!"

def parse_cowin_json(cjson):
	freeslots1 = 0;
	freeslots2 = 0;
	cen1 = [];
	cen2 = [];

	for centers in cjson['centers']:
		# print centers['sessions']
		for sessions in centers['sessions']:
			# print 'dose2 : ',type(sessions['available_capacity_dose2'])
			if sessions['available_capacity_dose2'] > 0 and sessions['vaccine'] == vaccine_type and sessions['min_age_limit'] == min_age_limit:
				freeslots2 = freeslots2 + 1
				cen1.append(centers)
				beep()
				# print("FS 0 : ",centers['sessions'], "\n")

			if sessions['available_capacity_dose1'] > 0 and sessions['vaccine'] == vaccine_type and sessions['min_age_limit'] == min_age_limit:
				freeslots1 = freeslots1 + 1
				cen1.append(centers)
				beep()
				# print("FS 1 : ",centers['sessions'], "\n")
	print("Time : ", datetime.now().strftime("%H:%M:%S"), " -- ", datetime.now().strftime("%d-%m-%Y"))
	print('Available slots for dose1 : %d' % (freeslots1))
	print('Available slots for dose2  : %d' % (freeslots2))

	for c in cen1:
		 print("First dose Slots: at ",c['name'], "\n address ", c['address'], "\n state : ", c['state_name'], "\n pincode : ", c['pincode'], "\n fee_type : " , c['fee_type'], "\n")
		 for s in c['sessions']:
		 	print ("details : \n\tavailable_capacity : ", s['available_capacity'], "\n\t min_age_limit : ", s['min_age_limit'], "\n\t vaccine type : ", s['vaccine'], "\n\t available_capacity_dose1 : ", s['available_capacity_dose1'], "\n\t available_capacity_dose2 : ", s['available_capacity_dose2']);


	for c in cen2:
		 print("Second dose Slots: at ",c['name'], "\n address ", c['address'], "\n state : ", c['state_name'], "\n pincode : ", c['pincode'], "\n fee_type : " , c['fee_type'], "\n")
		 for s in c['sessions']:
		 	print ("details : \n\tavailable_capacity : ", s['available_capacity'], "\n\t min_age_limit : ", s['min_age_limit'], "\n\t vaccine type : ", s['vaccine'], "\n\t available_capacity_dose1 : ", s['available_capacity_dose1'], "\n\t available_capacity_dose2 : ", s['available_capacity_dose2']);

def check_cowin_slots_for_district(districtId):
	headers = requests.utils.default_headers()
	headers.update(
	    {
	        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
	        'Content-type': 'application/json', 
	        'Accept': 'text/plain'
	    }
	)
	today = datetime.now().strftime("%d-%m-%Y")
	myparams = {'district_id':districtId, 'date':today }

	# "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=294&date=20-05-2021"
	# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content
	response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict', headers=headers, params=myparams )

	print("Status code: ", response.status_code)

	response_Json = response.json()

	if response.status_code == 200:
		# print(response_Json)
		print ("Available slots : \n\n")
		parse_cowin_json(response_Json)

while True:
    check_cowin_slots_for_district(294) # BBMP
    time.sleep(10)
    check_cowin_slots_for_district(265) # Bangalore Urban
    time.sleep(10)
