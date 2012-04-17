import datetime
from time import strftime

# Input file
inputFile = raw_input("Please provide the location (folder) of ZIPscannedData(B\W) for your trace: ")
userName = raw_input("Please enter the name of the user: ")
f = open(inputFile+'/ZIPscannedDataB').read()
lines = [line.strip(' ') for line in f.split('\n')]
lines.remove(lines[len(lines)-1])

# Output file
o = open(inputFile+'/experiment2_results_'+userName, 'w')
o.write('Trace Analysis for '+userName+'\n')
print '\nTrace Analysis for '+userName

# 1. Total Encounters
o.write('\n1. Total Encounters: '+str(len(lines)))
print '\n1. Total Encounters: '+str(len(lines))

# 2. Unique Encounters
o.write('\n2. Unique Encounters: '+str(len(set([line.split(';')[1] for line in lines]))))
print '\n2. Unique Encounters: '+str(len(set([line.split(';')[1] for line in lines])))

# 7. Distribution of Encounters by time
# Morning: 5:00am to 11:00am
# Afternoon: 11:01am to 17:00pm
# Evening: 17:01pm to 23:00pm
# Night: 23:01pm to 5:00am 
o.write("\n7. Encounters per time of the day :- ")
time_slices = [0 for i in range(4)]
for line in lines:
	hour = int(datetime.datetime.fromtimestamp(int(line.split(';')[0])).strftime("%H"))
	if (hour >= 23) and (hour < 5):
		time_slices[3] = time_slices[3]+1
	elif (hour >= 5) and (hour < 11):
		time_slices[0] = time_slices[0]+1
	elif (hour >=11) and (hour < 17):
		time_slices[1] = time_slices[1] + 1
	else:
		time_slices[2] = time_slices[2] + 1
o.write("Morning: "+str(time_slices[0])+" Afternoon: "+str(time_slices[1])+\
" Evening: "+str(time_slices[2])+" Night: "+str(time_slices[3])+'\n')

# 3. # of encounters per day vs time (in days)
o.write('\n3. Number of encounters per day :-\n')
days = []
[days.append(0) for i in range(366)]
for line in lines:
	timestamp = int(line.split(';')[0])
	doy = int(datetime.datetime.fromtimestamp(timestamp).strftime("%j"))
	for i in range(366):
		if i == doy:
			days[i] = days[i] + 1
for i in range(366):
	if days[i] > 0:
		o.write(str(datetime.datetime(2012, 1, 1)+datetime.timedelta(i-1))+','+str(days[i])+'\n')
		
# 12. Mac address
o.write("\n12. Unique Mac Addresses (Device Name) :-\n")
mac_addresses = []
for line in lines:
	arr = line.split(';')
	mac_add = arr[1]
	name = arr[2]
	word = name + '(' + mac_add +')'
	mac_addresses.append(word)
	
mac_addresses = list(set(mac_addresses))
o.write('\n'.join(mac_addresses))
		
# 4. # of encounters per device
o.write("\n\n4. Number of encounters per device :-\n")
devices = list(set([line.split(';')[2] for line in lines]))
encounters_per_device = []
[encounters_per_device.append(0) for device in devices]

for line in lines:
	arr = line.split(';')
	this_device = arr[2]
	for i in range(len(devices)):
		if this_device == devices[i]:
			encounters_per_device[i] = encounters_per_device[i] + 1
for i in range(len(devices)):
	o.write(devices[i] + ',' + str(encounters_per_device[i])+'\n')

# 5. Frequency of Access points (AP)
f = open(inputFile+'/ZIPscannedDataW').read()
lines = [line.strip(' ') for line in f.split('\n')]
lines.remove(lines[len(lines)-1])

o.write("\n\n5. Frequency of Access Points (AP) :-\n")
total_ap_encounters = [line.split(';')[2] for line in lines]
access_points = list(set(total_ap_encounters))
freq_access_points = [(ap,total_ap_encounters.count(ap)) for ap in access_points]

from operator import itemgetter
freq_access_points = sorted(freq_access_points, key=itemgetter(1), reverse=True)
count = 0

top_20_aps =[]
for i in range(len(freq_access_points)):
	if count > 19:
		break
	count = count + 1
	top_20_aps.append(freq_access_points[i][0])
	o.write(freq_access_points[i][0] + ',' + str(freq_access_points[i][1])+'\n')

# 6. Corresponding # of Bluetooth encounters per AP
encounters_top20_ap = [[] for i in range(20)]

for line in lines:
	arr = line.split(';')
	bluetooth = arr[1]
	this_ap = arr[2]
	for i in range(20):
		if this_ap == top_20_aps[i]:
			encounters_top20_ap[i].append(bluetooth)
for i in range(20):
	o.write(top_20_aps[i] + ',' + str(len(set(encounters_top20_ap[i])))+'\n')
# Close output file
o.close()
print "\nData points dumped in: " + inputFile+'/experiment2_results_'+userName