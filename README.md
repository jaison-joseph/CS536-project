
- Prerequisites
	- python3 (I used 3.10.2)
	- networkx install on python3
	- docker

- To run a simulation and generate a dataset, ust run:
`python3 master.py <number of nodes> [nsfnet/geant2/germany50] <number of runs per traffic intensity value> <time per run in SECONDS> <frequency of statistics in MILLISECONDS> <min traffic intensity> <max traffic intensity>`
	- the second argment: nsfnet/geant2/germany50 is the type of network, each one more densely connected than the other
	- the master.py orchestrates all the terminals to run the simulation
	- if:
		- number of runs per traffic intensity value is x
		- min traffic intensity is i
		- max traffic intensity is j
	- then:
		- the script runs a simulation x times for every value in the range [i, j] (both inclusive)
		- each run has the same test, same target bandwidths between runs
		- between different traffic intensities, the target bandwidths of connections vary
		- for every run, the topology and the link speeds of the links stay the same


- Here is the overview of what master.py does:
	- for each simulation (uasge of master.py), we start by randomly generating a topology and the required mininet topology file & ONOS config files
		- this is what the file main.py does, it is used once per simulation
		- this means that the topology and the bandwidths of the links in the virtual network are same throughout the entire simulation
		- we have a range of traffic intensity/lambda values that are also arguments to master.py (we collect a min and max traffic intensity value)
		- for each traffic intensity/lambda value in the user-provided range:
			- we generate a test file that uses d-itg commands to generate traffic between each pair of nodes, and record results
			- we do this once for each traffic intensity/lambda value, since its value determines indirectly target bandwidths for each pair of nodes in the test
			- then, we perform a series of runs for a given traffic intensity/lambda value; the number of runs is again an argment for master.py
			- we prepare for a series of runs by first setting up ONOS
				- this is only done once for a set of runs (for a given traffic intensity/lambda value)
				- ONOS is run in a docker container, to keep things as portable as possible
			- then, we set up mininet
				- mininet is also run in a docker container, to keep things as portable as possible
				- the mininet container also has d-itg installed for the test script
				- note that we setup ONOS and mininet in tmux windows to control them programatically
			- then, we run the test script n times, n being specified by the user
				- between each run, we use sed to change where the output of the test run is sent to
			- just before the last run has executed ( seconds before it finishes), we query ONOS to get the path between each pair of hosts.
				- the script for this is generated by main.py
			- and then we tear down the ONOS & mininet containers

	- the files are generated by `main.py` and `main_extension.py`
		- `main.py` generates everything except the test script `test.py`

	- look at the function `run_setup` in `master.py` to get the idea of what happens for a round of a simulation
	- the function `runner` does set up for a simulation

	- please note that the file "test.py" changes between runs: specifically the locations where the output raw filed and decoded files change

	- the output should look like:
	```
	simulations/
		<network_type>_<# nodes>_<min traffic intensity>_<max traffic intensity>/
			custom_topo.py
			get_hops.sh
			graph_attr.txt
			onos_config.json
			sorted_links.txt
			topo.json
			lambda_9/
				run_1/
					raw_data/
						2024-11-29-19:10:46.121925_4_4_0_1 
						2024-11-29-19:10:46.121925_4_4_0_2 
						2024-11-29-19:10:46.121925_4_4_0_3
						...
					decoded_data/
						2024-11-29-19:10:46.121925_4_4_0_1 
						2024-11-29-19:10:46.121925_4_4_0_2 
						2024-11-29-19:10:46.121925_4_4_0_3
						...
				run_2/
					...
			lambda_10/
				run_1/
					raw_data/
						2024-11-29-19:15:24.290317_4_4_0_1 
						2024-11-29-19:15:24.290317_4_4_0_2 
						2024-11-29-19:15:24.290317_4_4_0_3
						...
					decoded_data/
						2024-11-29-19:15:24.290317_4_4_0_1 
						2024-11-29-19:15:24.290317_4_4_0_2 
						2024-11-29-19:15:24.290317_4_4_0_3
						...
				run_2/
					...
	```