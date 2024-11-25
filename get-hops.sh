#!/bin/bash

curl -X GET http://localhost:8181/onos/v1/paths/device:s1/device:s2 -u onos:rocks >> paths.txt
echo >> paths.txt
curl -X GET http://localhost:8181/onos/v1/paths/device:s1/device:s3 -u onos:rocks >> paths.txt
echo >> paths.txt
curl -X GET http://localhost:8181/onos/v1/paths/device:s1/device:s4 -u onos:rocks >> paths.txt
echo >> paths.txt