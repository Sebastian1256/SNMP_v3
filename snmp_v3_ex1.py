# SNMP_ex1

from  snmp_helper import snmp_get_oid_v3, snmp_extract
from send_email import sendemail
import time , pygal , pickle
from datetime import datetime 


################################# Global Variables############################################

SNMP_Ports=[7961,8061]
IP = '50.242.94.227'
user = 'pysnmp' ; auth= 'galileo1'; encry='galileo1'
snmp_user=(user,auth,encry)
snmp_oid=(
	('ccmHistoryRunningLastChanged','1.3.6.1.4.1.9.9.43.1.1.1.0'),
	('Device_name','1.3.6.1.2.1.1.5.0'),
	)

from_addr='sebastianmarin1256@gmail.com'
to_addr_list='sebastian.marin@secureagility.com'
Login='xxxxxxx'
password='xxxxxxx'

'''
# Save  data the first time
router={}
while 1:
	try:
		for port in SNMP_Ports: 
			snmp_device=(IP,port)
			current_Run_Last_Changed = snmp_extract(snmp_get_oid_v3(snmp_device,snmp_user,snmp_oid[0][1]))
			Device_name = snmp_extract(snmp_get_oid_v3(snmp_device,snmp_user, snmp_oid[1][1]))
			router[Device_name]=[current_Run_Last_Changed]
		break
	except TypeError as e:
		print e
with open('Database.pickle_v2','wb') as Temp:
	pickle.dump(router,Temp)
'''


rtr_current={}
while 1:

	### open pickle file with store snmp values
	rtr_stored=pickle.load(open('Database.pickle_v2','rb'))

	### create try/except condition if there is timeout from evice
	try:
		for port in SNMP_Ports:


			### snmp_device get selected from the loop 
			snmp_device=(IP,port)

			### get current last changed as well as current device name 
			current_Run_Last_Changed = snmp_extract(snmp_get_oid_v3(snmp_device,snmp_user,snmp_oid[0][1]))
			Device_name = snmp_extract(snmp_get_oid_v3(snmp_device,snmp_user, snmp_oid[1][1]))
			
			### snmp values get appended into a dict 
			rtr_current[Device_name]=[current_Run_Last_Changed]
			print rtr_current
			print rtr_stored

			### Comparison takes place
			if rtr_stored[Device_name] < rtr_current[Device_name]:
				
				###  get the current time	
				Time=str(datetime.now())

				### create the subject and body of the email	
				subject='%s running config has changed at %s' % (Device_name,Time)
				message='''
						Hello Sebastian\n 

						Router %s running configuration has changed to %s .\n
		

						Regards\n
						Sebastian''' % (Device_name,current_Run_Last_Changed)

				### send email to myself or other account 
				sendemail(from_addr,to_addr_list,'',subject,message,Login,password)

				### update the stored snmp value and save it into a prior pickle file
				rtr_stored[Device_name]=rtr_current[Device_name]	
				with open ('Database.pickle_v2','wb') as Temp:
					pickle.dump(rtr_stored,Temp)


	except TypeError as e:
		print e
