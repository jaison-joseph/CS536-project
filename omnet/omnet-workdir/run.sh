#!/bin/bash

# 1. Create project structure
cd nsfnet_simulation

# 2. Copy the files we created above into src/

# 3. Initialize OMNeT++ project
opp_makemake -f --deep -O out -KINET_PROJ=/path/to/inet -DINET_IMPORT 
make

# 4. Run the simulation
./nsfnet -u Cmdenv  # For command-line mode