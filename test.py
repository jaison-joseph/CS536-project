def run_tests(net):
	from datetime import datetime
	# Create logs directory if it doesn't exist
	if not os.path.exists('logs'):
		os.makedirs('logs')

	# Get current timestamp for log files
	timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')


	# Get host objects
	h0, h1, h2, h3, h4 = net.get('h0', 'h1', 'h2', 'h3', 'h4')

	try:
		# start ditg servers
		h0.cmd('nohup ITGRecv &')
		h1.cmd('nohup ITGRecv &')
		h2.cmd('nohup ITGRecv &')
		h3.cmd('nohup ITGRecv &')
		h4.cmd('nohup ITGRecv &')
		
		# wait for servers to start
		time.sleep(2)
		
		# run iperf clients
		h4.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.10867 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_4_2.txt 2>&1 &')
		h4.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.68351 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_4_3.txt 2>&1 &')
		h4.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.69830 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_4_1.txt 2>&1 &')
		h1.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.69663 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_1_4.txt 2>&1 &')
		h1.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.93200 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_1_2.txt 2>&1 &')
		h2.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.29841 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_2_3.txt 2>&1 &')
		h3.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.54389 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_3_0.txt 2>&1 &')
		h2.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.63563 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_2_0.txt 2>&1 &')
		h0.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.38016 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_0_1.txt 2>&1 &')
		h1.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.35459 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_1_3.txt 2>&1 &')
		h3.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.68177 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_3_4.txt 2>&1 &')
		h2.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.71170 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_2_4.txt 2>&1 &')
		h0.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.71253 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_0_4.txt 2>&1 &')
		h0.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.01245 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_0_2.txt 2>&1 &')
		h1.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.85399 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_1_0.txt 2>&1 &')
		h3.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.23889 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_3_1.txt 2>&1 &')
		h2.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.67042 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_2_1.txt 2>&1 &')
		h4.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.70462 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_4_0.txt 2>&1 &')
		h3.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.07500 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_3_2.txt 2>&1 &')
		h0.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.86412 -t 120000 -x logs/2024-11-26-10:32:11.299315_0_0_0_3.txt 2>&1 &')
		
		# wait for ITGSend to finish
		time.sleep(240)
		
		# Kill ITGRecv servers
		h0.cmd('killall ITGRecv')
		h1.cmd('killall ITGRecv')
		h2.cmd('killall ITGRecv')
		h3.cmd('killall ITGRecv')
		h4.cmd('killall ITGRecv')
		
		# wait for killing of ITGRecv processes
		time.sleep(2)
		
		# decode d-itg logs to 10-second interval stats
		h4.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_4_2.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_4_2.txt 2>&1 &')
		h4.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_4_3.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_4_3.txt 2>&1 &')
		h4.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_4_1.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_4_1.txt 2>&1 &')
		h1.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_1_4.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_1_4.txt 2>&1 &')
		h1.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_1_2.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_1_2.txt 2>&1 &')
		h2.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_2_3.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_2_3.txt 2>&1 &')
		h3.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_3_0.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_3_0.txt 2>&1 &')
		h2.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_2_0.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_2_0.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_0_1.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_0_1.txt 2>&1 &')
		h1.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_1_3.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_1_3.txt 2>&1 &')
		h3.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_3_4.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_3_4.txt 2>&1 &')
		h2.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_2_4.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_2_4.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_0_4.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_0_4.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_0_2.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_0_2.txt 2>&1 &')
		h1.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_1_0.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_1_0.txt 2>&1 &')
		h3.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_3_1.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_3_1.txt 2>&1 &')
		h2.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_2_1.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_2_1.txt 2>&1 &')
		h4.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_4_0.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_4_0.txt 2>&1 &')
		h3.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_3_2.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_3_2.txt 2>&1 &')
		h0.cmd('nohup ITGDec logs/2024-11-26-10:32:11.299315_0_0_0_3.txt -c 1000 decoded/2024-11-26-10:32:11.299315_0_0_0_3.txt 2>&1 &')
		
	except Exception as e:
		return 1

# this file is executed from the mininet shell; this is how to use it:
# mininet> py execfile('test.py')
# mininet> py run_tests(net)
