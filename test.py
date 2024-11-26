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
		h0.cmd('nohup ITGRecv &')
		h1.cmd('nohup ITGRecv &')
		h2.cmd('nohup ITGRecv &')
		
		# wait for servers to start
		time.sleep(2)
		
		# run iperf clients
		h2.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.12804 -t 120000 -x logs/2024-11-26-09:52:53.840419_0_0_2_0.txt 2>&1 &')
		h0.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.84172 -t 120000 -x logs/2024-11-26-09:52:53.840419_0_0_0_2.txt 2>&1 &')
		h2.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 4.89500 -t 120000 -x logs/2024-11-26-09:52:53.840419_0_0_2_1.txt 2>&1 &')
		h1.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.55205 -t 120000 -x logs/2024-11-26-09:52:53.840419_0_0_1_2.txt 2>&1 &')
		h0.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.62105 -t 120000 -x logs/2024-11-26-09:52:53.840419_0_0_0_1.txt 2>&1 &')
		h1.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 3.61631 -t 120000 -x logs/2024-11-26-09:52:53.840419_0_0_1_0.txt 2>&1 &')
		
		# wait for ITGSend to finish
		time.sleep(240)
		
		# Kill ITGRecv servers
		h0.cmd('killall ITGRecv')
		h1.cmd('killall ITGRecv')
		h2.cmd('killall ITGRecv')
		
		# wait for killing of ITGRecv processes
		time.sleep(2)
		
		# decode d-itg logs to 10-second interval stats
		h2.cmd('nohup ITGDec logs/2024-11-26-09:52:53.840419_0_0_2_0.txt -c 1000 decoded/2024-11-26-09:52:53.840419_0_0_2_0.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-09:52:53.840419_0_0_0_2.txt -c 1000 decoded/2024-11-26-09:52:53.840419_0_0_0_2.txt 2>&1 &')
		h2.cmd('nohup ITGDec logs/2024-11-26-09:52:53.840419_0_0_2_1.txt -c 1000 decoded/2024-11-26-09:52:53.840419_0_0_2_1.txt 2>&1 &')
		h1.cmd('nohup ITGDec logs/2024-11-26-09:52:53.840419_0_0_1_2.txt -c 1000 decoded/2024-11-26-09:52:53.840419_0_0_1_2.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-09:52:53.840419_0_0_0_1.txt -c 1000 decoded/2024-11-26-09:52:53.840419_0_0_0_1.txt 2>&1 &')
		h1.cmd('nohup ITGDec logs/2024-11-26-09:52:53.840419_0_0_1_0.txt -c 1000 decoded/2024-11-26-09:52:53.840419_0_0_1_0.txt 2>&1 &')
		
	except Exception as e:
		return 1

# this file is executed from the mininet shell; this is how to use it:
# mininet> py execfile('test.py')
# mininet> py run_tests(net)
