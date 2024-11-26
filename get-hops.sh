#!/bin/bash

echo "(s0, s1): $(curl -X GET http://localhost:8181/onos/v1/paths/device:s0/device:s1 -u onos:rocks)" >> paths.txt
echo "(s0, s2): $(curl -X GET http://localhost:8181/onos/v1/paths/device:s0/device:s2 -u onos:rocks)" >> paths.txt
echo "(s1, s0): $(curl -X GET http://localhost:8181/onos/v1/paths/device:s1/device:s0 -u onos:rocks)" >> paths.txt
echo "(s1, s2): $(curl -X GET http://localhost:8181/onos/v1/paths/device:s1/device:s2 -u onos:rocks)" >> paths.txt
echo "(s2, s0): $(curl -X GET http://localhost:8181/onos/v1/paths/device:s2/device:s0 -u onos:rocks)" >> paths.txt
echo "(s2, s1): $(curl -X GET http://localhost:8181/onos/v1/paths/device:s2/device:s1 -u onos:rocks)" >> paths.txt
