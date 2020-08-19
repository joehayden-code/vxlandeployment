import yaml, os, sys
from pprint import pprint

spinedict = {}
config = ""

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
				if k4 == 'spines':
					for k5, v5 in v4.items():
						spine_name = k5
						for k6, v6 in v5.items():
							if k6 == 'port':
								spineport = str(v6)
							if k6 == 'description':
								spinedesc = str(v6)
							if k6 == 'ipaddress':
								spineipaddr = v6
						tempdict = {spine_name: {
						'spine_if': spineport,
						'spine_if_desc': spinedesc,
						'spine_if_ipaddr': spineipaddr
						}}
						spinedict.update(tempdict)
						

# Build Spine script

def build_spine_config(name, intf, desc, ip):
	
	spineconfig = "***** Configuration for " + name + " *****\n"
	spineconfig = spineconfig + "interface " + intf + "\n"
	spineconfig = spineconfig + "description" + desc + "\n"
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
	spineconfig = spineconfig + "ip pim sparse mode\n\n"

	return spineconfig


# Build spine configuration
for switch, swconfig in spinedict.items():
	for key, value in swconfig.items():
		if key == 'spine_if':
			intf = value
		if key == 'spine_if_desc':
			desc = value
		if key == 'spine_if_ipaddr':
			ip = value
	config = config + build_spine_config (switch, intf, desc, ip)


print (config)



print()
print('**********')
print()
pprint (spinedict)