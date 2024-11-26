
- I have modified parts the setup scripts from the CS536 setup for use in the final project. Here are the updated steps. 
They assume that you are running on a t2.large EC2 instance

- Unzip the folder, cd into it from the terminal.
	- To create the topology file (`custom-topo.py`) and the test file (`test.py`), look at the comments in the file `main.py`: it sets up both in 1 step.
	- `main.py` has commands to define the configuration and setup pairs of hosts to test as well.
	- `custom-topo.py` is used by `scripts/mn-custom`, and we will manually execute `test.py` from the mininet shell

- In the terminal window, navigate into the downloaded folder. Then, run:
`make controller`

- In another terminal window, navigate into the downloaded folder. Then, run:
`make mininet`
	- Once the above has run, you should see the mininet CLI. From it, run 
		`net`
	to see the list of hosts. You should see all of them. 

- In another terminal window, navigate into the downloaded folder. Then, run:
`make cli`
	- Once the above has run, you should see the ONOS CLI. From the ONOS CLI, run the below command:
	`app activate fwd`

- In another terminal window, navigate into the downloaded folder. Then, run:
`make netcfg`

- Now, the setup should be complete. 

- If you navigate to the shell where mininet is running, run `pingall`: the results should match what you expect to see given the network configuration. Now, to run the `test.py` file and get the network metrics, run the following commands in the specified order:
	- ```shell
		mininet> py execfile('test.py')
		mininet> py run_tests(net) 
		```
	- the output will appear in the `logs/` directory
	- the format of the output file is: `2024-11-22-19:09:45.291079_4_4_1_2` : `<date>-<time>_<number of hosts>_<number of switches>_<client host number>_<server host number>`
- Manual metrics collection
The setup has iperf3 (better version of iperf with more statistics built-in) installed on the mininet hosts; from the mininet CLI you should be able to run: <br>
	- `h1 iperf3 -s &` # start iperf3 server at h1 <br>
	- `h2 iperf3 -c h1 -u -l 1000 -t 15 -i 1` # use UDP (-u) for 15 seconds (-t 15) sending 1000 byte packets (-l 1000) between h1 and h2 to get network statistics, printing stats every 1 second (-i 1) <br>
	- `h1 killall iperf3` # kill the iperf3 server at h1
	``````
	mininet> h1 iperf3 -s &     
	-----------------------------------------------------------
	Server listening on 5201
	-----------------------------------------------------------
	mininet> h2 iperf3 -c h1 -u -l 1000 -t 15 -i 1
	Connecting to host 10.0.0.1, port 5201
	[  4] local 10.0.0.2 port 45648 connected to 10.0.0.1 port 5201
	[ ID] Interval           Transfer     Bandwidth       Total Datagrams
	[  4]   0.00-1.00   sec   116 KBytes   952 Kbits/sec  119  
	[  4]   1.00-2.00   sec   129 KBytes  1.06 Mbits/sec  132  
	[  4]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]  10.00-11.00  sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]  11.00-12.00  sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]  12.00-13.00  sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]  13.00-14.00  sec   128 KBytes  1.05 Mbits/sec  131  
	[  4]  14.00-15.00  sec   129 KBytes  1.06 Mbits/sec  132  
	- - - - - - - - - - - - - - - - - - - - - - - - -
	[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
	[  4]   0.00-15.00  sec  1.86 MBytes  1.04 Mbits/sec  0.979 ms  767/1955 (39%)  
	[  4] Sent 1955 datagrams
	``````
	- which should give you bandwidth, jitter, and loss statistics between h1 and h2
	- the point of `test.py` is to automate this, for any number of hosts you wish to test in a given network setup.
