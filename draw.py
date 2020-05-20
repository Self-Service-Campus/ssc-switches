

def draw_vlan():
	switches = Switch.objects.all()
	vlans = {}
	for switch in switches:
		ports = Port.objects.get(switch=switch)
		for port in ports:
			if 'up' in port.link_status:
				for vlan in port.trunking_vlans:
					if vlan in vlans:
						vlans[vlan] = vlans[vlan].append(vlan)
					else:
						vlans[vlan] = [vlan]
	return vlans
