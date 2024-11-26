def run_tests(net):
	from datetime import datetime
	# Create logs directory if it doesn't exist
	if not os.path.exists('logs'):
		os.makedirs('logs')

	# Get current timestamp for log files
	timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')


	# Get host objects
	h0, h1, h2 = net.get('h0', 'h1', 'h2')

	try:
		# start ditg servers
		print('starting ditg server @ 0')
		h0.cmd('nohup ITGRecv &')
		print('starting ditg server @ 1')
		h1.cmd('nohup ITGRecv &')
		print('starting ditg server @ 2')
		h2.cmd('nohup ITGRecv &')
		
		# wait for servers to start
		print('wait for servers to start')
		time.sleep(2)
		
		# run iperf clients
		print('run iperf clients')
		print('launching 1 -> 2 ITGSend')
		h1.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.58496 -t 15000 -x logs/2024-11-26-08:30:30.372902_0_0_1_2.txt 2>&1 &')
		print('launching 2 -> 0 ITGSend')
		h2.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 7.54596 -t 15000 -x logs/2024-11-26-08:30:30.372902_0_0_2_0.txt 2>&1 &')
		print('launching 1 -> 0 ITGSend')
		h1.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 7.50934 -t 15000 -x logs/2024-11-26-08:30:30.372902_0_0_1_0.txt 2>&1 &')
		print('launching 0 -> 2 ITGSend')
		h0.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 4.80207 -t 15000 -x logs/2024-11-26-08:30:30.372902_0_0_0_2.txt 2>&1 &')
		print('launching 2 -> 1 ITGSend')
		h2.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 7.03440 -t 15000 -x logs/2024-11-26-08:30:30.372902_0_0_2_1.txt 2>&1 &')
		print('launching 0 -> 1 ITGSend')
		h0.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.63743 -t 15000 -x logs/2024-11-26-08:30:30.372902_0_0_0_1.txt 2>&1 &')
		
		# wait for ITGSend to finish
		print('wait for ITGSend to finish')
		time.sleep(30)
		
		# Kill ITGRecv servers
		print('Kill ITGRecv servers')
		h0.cmd('killall ITGRecv')
		h1.cmd('killall ITGRecv')
		h2.cmd('killall ITGRecv')
		
		# wait for killing of ITGRecv processes
		print('wait for killing of ITGRecv processes')
		time.sleep(2)
		
		# decode d-itg logs to 10-second interval stats
		h1.cmd('nohup ITGDec logs/2024-11-26-08:30:30.372902_0_0_1_2.txt -c 1000 decoded/2024-11-26-08:30:30.372902_0_0_1_2.txt 2>&1 &')
		h2.cmd('nohup ITGDec logs/2024-11-26-08:30:30.372902_0_0_2_0.txt -c 1000 decoded/2024-11-26-08:30:30.372902_0_0_2_0.txt 2>&1 &')
		h1.cmd('nohup ITGDec logs/2024-11-26-08:30:30.372902_0_0_1_0.txt -c 1000 decoded/2024-11-26-08:30:30.372902_0_0_1_0.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-08:30:30.372902_0_0_0_2.txt -c 1000 decoded/2024-11-26-08:30:30.372902_0_0_0_2.txt 2>&1 &')
		h2.cmd('nohup ITGDec logs/2024-11-26-08:30:30.372902_0_0_2_1.txt -c 1000 decoded/2024-11-26-08:30:30.372902_0_0_2_1.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-08:30:30.372902_0_0_0_1.txt -c 1000 decoded/2024-11-26-08:30:30.372902_0_0_0_1.txt 2>&1 &')
		
	except Exception as e:
		print(e)

# this file is executed from the mininet shell; this is how to use it:
# mininet> py execfile('test.py')
# mininet> py run_tests(net)
