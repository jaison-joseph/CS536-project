############################################################################
##
##     CS536 final project makefile
##
##  
##
#############################################################################

SCRIPTS = scripts/

export name ?=
# export ONOS_CONFIG_FILE ?=

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
ifndef MN_STRATUM_TOPO_FILE
	$(error MN_STRATUM_TOPO_FILE is required. Usage: make netcfg MN_STRATUM_TOPO_FILE=path/to/config.json)
endif
	$(SCRIPTS)/mn-custom MN_STRATUM_TOPO_FILE=$(MN_STRATUM_TOPO_FILE)

controller:
	ONOS_APPS=gui,proxyarp,drivers.bmv2,lldpprovider,hostprovider,fwd,openflow \
	$(SCRIPTS)/onos

cli:
	$(SCRIPTS)/onos-cli

# netcfg:
# 	$(SCRIPTS)/onos-netcfg cfg/netcfg.json

netcfg:
ifndef ONOS_CONFIG_FILE
	$(error ONOS_CONFIG_FILE is required. Usage: make netcfg ONOS_CONFIG_FILE=path/to/config.json)
endif
	$(SCRIPTS)/onos-netcfg $(ONOS_CONFIG_FILE)

# Usage: make host name=h1
host:
	$(SCRIPTS)/utils/mn-stratum/exec $(name)

