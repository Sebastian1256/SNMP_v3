# SNMP_ex2


from  snmp_helper import snmp_get_oid_v3, snmp_extract
from email_helper import send_mail
import time , pygal


SNMP_Ports=[7961,8061]
IP = '50.242.94.227'
user = 'pysnmp' ; auth= 'galileo1'; encry='galileo1'

snmp_device=(IP,SNMP_Ports[1])
snmp_user=(user,auth,encry)



snmp_oids=(
    #('sysUptime','1.3.6.1.2.1.1.3.0'),
    #('ifDescri_fa4' ,'1.3.6.1.2.1.2.2.1.2.5'),
    ('ifInOctects_fa4' ,'1.3.6.1.2.1.2.2.1.10.5'),
    ('ifInUcatsPkts_fa4','1.3.6.1.2.1.2.2.1.11.5'),
    ('ifOutOctects_fa4','1.3.6.1.2.1.2.2.1.16.5'),
    ('ifOutUcastPkts_fa4','1.3.6.1.2.1.2.2.1.17.5'),
    )



rtr_info={}
Fa4_InOctects=[]
Fa4_InUcast=[]
Fa4_OutOctects=[]
Fa4_OutUcast=[]
delay=3000
x_label=[]
counter=1
limiter=12


### stay in the loop until 60 minutes
while counter < limiter:

    ### get snmp values for rtr1 if  timeout occurs, raise an error and try again
    while 1:
        try:
            for des,oid in snmp_oids:
                out = snmp_extract(snmp_get_oid_v3(snmp_device,snmp_user, oid))
                print '%s %s' % (des , out)
                rtr_info[des]=out
            break
        except TypeError:
            print 'error'
    
    ### once we obtain values, it is appended into lists
    Fa4_InOctects.append(int(rtr_info['ifInOctects_fa4']))
    Fa4_InUcast.append(int(rtr_info['ifInUcatsPkts_fa4']))
    Fa4_OutOctects.append(int(rtr_info['ifOutOctects_fa4']))
    Fa4_OutUcast.append(int(rtr_info['ifOutUcastPkts_fa4']))
    
    ### sleep for five minutes
    time.sleep(delay)

    ### multiple the time for counter and create the time label for graph
    x_axis=delay*counter
    x_label.append(str(x_axis))
    counter+=1
   


    ### create graph 1 and 2
    line_chart_1=pygal.Line()
    line_chart_2=pygal.Line()
    line_chart_1.title = 'Input/Output Bytes'
    line_chart_2.title = 'Input/Output Packet'
    line_chart_1.x_labels=x_label
    line_chart_2.x_labels=x_label

    line_chart_1.add('InBytes', Fa4_InOctects)
    line_chart_1.add('OutBytes', Fa4_OutOctects)
    line_chart_2.add('InPackets', Fa4_InUcast)
    line_chart_2.add('OutPackets', Fa4_OutUcast)
    
    line_chart_1.render_to_file('I_O_bytes.svg')
    line_chart_2.render_to_file('I_O_packets.svg')
