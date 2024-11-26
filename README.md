
- I have modified parts the setup scripts from the CS536 setup for use in the final project. Here are the updated steps. 
They assume that you are running on a t2.large EC2 instance

- Unzip the folder, cd into it from the terminal.
	- To create the mininet topology file (`custom-topo.py`), the ONOS config file (`cfg/onos_config.json`) and the D-ITG test file (`test.py`), run this command:
		```shell
		python3 main.py <number of hosts> <number of switches> nsfnet && python3 main_extension.py
		```
	- `main.py` along with `main_extension.py` has commands to define the configuration and setup pairs of hosts to test as well.
	- `custom-topo.py` is used by `scripts/mn-custom`, and we will manually execute `test.py` from the mininet shell
	- technically, one can use one of (nsfnet, geant2, germany50) but only nsfnet is kinda tested
		- I have only tested output of main.py with the following # of (hosts, switches):
			- (3, 3)
			- (4, 4)
			- (5, 5)
			- Other values should work, I just haven't tested it yet

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

- If you navigate to the shell where mininet CLI is running, run `pingall`: the results should match what you expect to see given the network configuration. Now, to run the `test.py` file and get the network metrics, run the following commands in the specified order:
	- ```shell
		mininet> py execfile('test.py')
		mininet> py run_tests(net) 
		```
	- the output will appear in the `decoded/` directory
	- the format of the output file is: `2024-11-22-19:09:45.291079_4_4_1_2` : `<date>-<time>_<number of hosts>_<number of switches>_<client host number>_<server host number>`
- Manual metrics collection
The setup has iperf3 (better version of iperf with more statistics built-in) installed on the mininet hosts; from the mininet CLI you should be able to run: <br>
	- `h0 ITGRecv &` # start ITGRecv process at h0 <br>
	- `h1 ITGSend -a 10.0.0.1 -T UDP -c 100 -C 10 -t 10000 -x logs/h1-receiver.log` # use UDP (-T UDP) for 15 seconds (-t 10000) sending 100 byte packets (-c 100) between h0 (10.0.0.1) and h1, outputting the raw data to `logs/h1-receiver.log`
	- `h0 killall ITGRecv` # kill the ITGRecv process at h0
	- `h1 ITGDec logs/h1-receiver.log -c 1000 decoded/h1-receiver.log` # decode the raw data in `logs/h1-receiver.log` to `decoded/h1-receiver.log`, outputting summary statistics of every 1 second (-c 1000) 
	- the output of a file in the `decoded` directory should look like:
	``````
	0.000000 4.320000 0.283413 0.334594 4.000000
	1.000000 3.712000 0.002269 0.000634 1.000000
	2.000000 0.912000 1.006080 0.338009 4.000000
	3.000000 2.312000 0.990367 0.024039 2.000000
	4.000000 2.616000 0.515318 0.475159 5.000000
	5.000000 3.712000 0.001757 0.000200 1.000000
	6.000000 0.608000 0.114292 0.368459 4.000000
	7.000000 2.312000 0.189412 0.042548 4.000000
	8.000000 1.704000 0.001547 0.000255 1.000000
	9.000000 4.320000 0.323090 0.142764 5.000000
	10.000000 5.416000 0.001520 0.000111 1.000000
	11.000000 0.608000 0.121973 0.384080 4.000000
	12.000000 2.008000 0.088707 0.114492 1.000000
	13.000000 2.312000 0.003753 0.000256 5.000000
	14.000000 2.008000 0.001622 0.000119 0.000000
	15.000000 2.008000 0.001515 0.000339 1.000000
	16.000000 5.112000 0.001719 0.000151 6.000000
	17.000000 2.312000 0.003304 0.000344 3.000000
	...
	``````
	- the 5 statistics in each row are: Time, Bitrate, Delay, Jitter, Packet loss
	- the point of `test.py` is to automate this, for any number of hosts you wish to test in a given network setup.

- Alternatively, if you want to do everything in the above steps, just run:
`python3 master.py <number of hosts> <number of switches> nsfnet`
	- this unfortunately causes mininet/the mininet container to often throw some exception 