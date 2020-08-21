import yaml, os, sys
from pprint import pprint

spinedict = {}
config = ""
sjcx_spines = ['sjx1-spine-1', 'sjx1-spine-2', 'sjx1-spine-3', 'sjx1-spine-4']
ascx_spines = ['asx1-spine-1', 'asx1-spine-2', 'asx1-spine-3', 'asx1-spine-4']
sjcx_bdleaf = ['sjx1-bsleaf-1', 'sjx1-bsleaf-2']
ascx_bdleaf = ['asx1-bsleaf-1', 'sjx1-bsleaf-2']
switch_counter = 1
rack_counter = 1

with open('pod.yaml') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

# Parse the YAML Configuration
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
				if k4 == 'racks':
					racks = int(v4)
				if k4 == 'spines':
					for k5, v5 in v4.items():
						if k5 == 'port':
							spineport = str(v5)
						if k5 == 'description':
							spinedesc = str(v5)
						if k5 == 'ipaddress':
							spineipaddr = str(v5)
						

# Build Spine Configuration
def build_spine_config(name, intf, desc, ip, pod):
	
	spineconfig = "***** Configuration for " + name + " for " + pod + " *****\n"
	spineconfig = spineconfig + "interface " + intf + "\n"
	spineconfig = spineconfig + "description " + desc + "\n"
	spineconfig = spineconfig + "mtu 9216\n"
	spineconfig = spineconfig + "link debounce time 0\n"
	spineconfig = spineconfig + "medium p2p\n"
	spineconfig = spineconfig + "no ip redirects\n"
	spineconfig = spineconfig + "ip address " + ip + "\n"
	spineconfig = spineconfig + "no ipv6 redirects\n"
	spineconfig = spineconfig + "ip ospf authentication message-digest\n"
	spineconfig = spineconfig + "ip ospf message-digest-key 1 md5 3 blabbabaablalbla\n"
	spineconfig = spineconfig + "ip ospf network point-to-point\n"
	spineconfig = spineconfig + "no ip ospf passive interface\n"
	spineconfig = spineconfig + "ip router ospf 1 area 0.0.0.0\n"
	spineconfig = spineconfig + "ip pim sparse mode\n"
	spineconfig = spineconfig + "shut\n\n\n"

	return spineconfig

#Increment last IP address
def increment_ip(address, incrementor):
	
	network = address.split('/')
	octet = network[0].split('.')
	step = incrementor * 4 - 4
	new_network = octet[0] + "." + octet[1] + "." + octet[2] + "." + str(int(octet[3]) + step) + "/" + network[1]

	return new_network

# Choose the spine list based on site
if site == 'SJCX':
	spine_list = sjcx_spines
	bdleaf_list = sjcx_bdleaf
if site == 'ASCX':
	spine_list = ascx_spines
	bdleaf_list = ascx_bdleaf


while rack_counter <= racks:

	rack_name = site + '-' + "!"

	for spine in spine_list:

		if spine[-1] == '1':
			config = build_spine_config(spine, spineport, spinedesc, increment_ip(spineipaddr, switch_counter), podname)
			print (config)
		if spine[-1] == '2':
			config = build_spine_config(spine, spineport, spinedesc, increment_ip(spineipaddr, switch_counter), podname)
			print (config)
		if spine[-1] == '3':
			config = build_spine_config(spine, spineport, spinedesc, increment_ip(spineipaddr, switch_counter), podname)
			print (config)
		if spine[-1] == '4':
			config = build_spine_config(spine, spineport, spinedesc, increment_ip(spineipaddr, switch_counter), podname)
			print (config)

		switch_counter += 1

	switch_counter = 1
	rack_counter += 1

