import yaml, os, sys
from pprint import pprint

with open('pod.yaml') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

# Grab the site info
for k1, v1 in data.items():
	site = k1
	# Loop through pod info
	for k2, v2 in v1.items():
		# Loop through vars
		for k3, v3 in v2.items():
			# Get pod data
			for k4, v4 in v3.items():
				if k4 == 'name':
					podname = str(v4)
				if k4 == 'pod_mgt_vlan':
					podmgtvlan = str(v4)
				if k4 == 'pod_mgt_net':
					podmgtnet = str(v4)
				if k4 == 'pod_mgt_mcast_grp':
					podmgtnet = str(v4)
				if k4 == 'esxi_vmotion_vlan':
					esxivmotionvlan = str(v4)
				if k4 == 'esxi_vmotion_network':
					esxivmotionnetwork = str(v4)
				if k4 == 'esxi_vmotion_mcast_grp':
					esxivmotionmcast = str(v4)
				if k4 == 'spines':
					for k5, v5 in v4.items():
						switchname = k5
						for k6, v6 in v5.items():
							if k6 == 'port':
								spineport = str(v6)
							if k6 == 'description':
								spinedesc = str(v6)
							if k6 == 'ipaddress':
								spineipaddr = v6
						print("  " + switchname)
						print ("    " + spineport)
						print ("    " + spinedesc)
						print ("    " + spineipaddr)
						print ()
			print (podname)
			print ("  " + podmgtvlan)
			print ("  " + podmgtnet)
			print ("  " + esxivmotionvlan)
			print ("  " + esxivmotionnetwork)
			print ("  " + esxivmotionmcast)



print()
print('**********')
print()
pprint (data)