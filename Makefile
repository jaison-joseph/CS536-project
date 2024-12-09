############################################################################
##
##     CS536 final project makefile
##
##  
##
#############################################################################

SCRIPTS = scripts/

export name ?=

.PHONY: mininet controller cli netcfg

mininet:
ifndef MN_STRATUM_TOPO_FILE
	$(error MN_STRATUM_TOPO_FILE is required. Usage: make mininet MN_STRATUM_TOPO_FILE=path/to/config.json)
endif
	$(SCRIPTS)/mn-custom MN_STRATUM_TOPO_FILE=$(MN_STRATUM_TOPO_FILE)

controller:
	ONOS_APPS=gui,proxyarp,drivers.bmv2,lldpprovider,hostprovider,fwd,openflow \
	$(SCRIPTS)/onos

cli:
	$(SCRIPTS)/onos-cli

# Usage: make host name=h1
host:
	$(SCRIPTS)/utils/mn-stratum/exec $(name)

