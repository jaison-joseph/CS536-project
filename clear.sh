#!/bin/sh

tmux kill-server
docker rm -f onos 
docker rm -f onos-cli 
docker rm -f mn-stratum 