############################################################################
##
##     CS536 final project makefile
##
##  
##
#############################################################################

SCRIPTS = scripts/

export name ?=

.PHONY: mininet mininet-install-iperf3 controller cli netcfg

help: 
	@echo "Example usage ...\n"
	@echo "- Start Mininet: make mininet\n"
	@echo "- Install Mininet Prereqs/Dependencies: make mininet-install-iperf3\n"
	@echo "- Start Controller: make controller\n"
	@echo "- Controller CLI: make cli (password is rocks)\n"
	@echo "- Connect Controller to Mininet: make netcfg\n"
	@echo "- Access Host: make host name=h1\n"

# mininet:
# 	$(SCRIPTS)/mn-stratum --topo linear,2

# mininet:
# 	$(SCRIPTS)/mn-stratum --custom custom-topo.py --topo customtopo --link tc

mininet-install-iperf3:
	docker exec -it mn-stratum bash -c \
		"sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list ; \
		sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list ; \
		sed -i '/stretch-updates/d' /etc/apt/sources.list ; \
		apt-get --allow-insecure-repositories --allow-unauthenticated update ; \
		apt-get -y --allow-unauthenticated install iperf3"

mininet:
	$(SCRIPTS)/mn-custom

controller:
	ONOS_APPS=gui,proxyarp,drivers.bmv2,lldpprovider,hostprovider,fwd \
	$(SCRIPTS)/onos

cli:
	$(SCRIPTS)/onos-cli

# netcfg:
# 	$(SCRIPTS)/onos-netcfg cfg/netcfg.json

netcfg:
	$(SCRIPTS)/onos-netcfg cfg/netcfg.json

# Usage: make host name=h1
host:
	$(SCRIPTS)/utils/mn-stratum/exec $(name)

