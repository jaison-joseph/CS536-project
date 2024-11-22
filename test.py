def run_tests(net):
	from datetime import datetime
	# Create logs directory if it doesn't exist
	if not os.path.exists('logs'):
		os.makedirs('logs')

	# Get current timestamp for log files
	timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')


	# Get host objects
	h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')

	try:
		# start iperf servers
		print('starting 3 iperf server(s) @ 1')
		h1.cmd('iperf3 -s -p 5101&')
		h1.cmd('iperf3 -s -p 5102&')
		h1.cmd('iperf3 -s -p 5103&')
		print('starting 3 iperf server(s) @ 2')
		h2.cmd('iperf3 -s -p 5101&')
		h2.cmd('iperf3 -s -p 5102&')
		h2.cmd('iperf3 -s -p 5103&')
		print('starting 3 iperf server(s) @ 3')
		h3.cmd('iperf3 -s -p 5101&')
		h3.cmd('iperf3 -s -p 5102&')
		h3.cmd('iperf3 -s -p 5103&')
		print('starting 3 iperf server(s) @ 4')
		h4.cmd('iperf3 -s -p 5101&')
		h4.cmd('iperf3 -s -p 5102&')
		h4.cmd('iperf3 -s -p 5103&')
		
		# wait for servers to start
		print('wait for servers to start')
		time.sleep(2)
		
		# run iperf clients
		print('run iperf clients')
		print('launching 1 -> 3 iperf')
		h1.cmd('nohup iperf3 -c 10.0.0.3 -u -b 1M -t 15 -p 5103 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_1_3.txt 2>&1 &')
		print('launching 2 -> 4 iperf')
		h2.cmd('nohup iperf3 -c 10.0.0.4 -u -b 1M -t 15 -p 5103 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_2_4.txt 2>&1 &')
		print('launching 1 -> 2 iperf')
		h1.cmd('nohup iperf3 -c 10.0.0.2 -u -b 1M -t 15 -p 5103 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_1_2.txt 2>&1 &')
		print('launching 2 -> 1 iperf')
		h2.cmd('nohup iperf3 -c 10.0.0.1 -u -b 1M -t 15 -p 5103 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_2_1.txt 2>&1 &')
		print('launching 3 -> 4 iperf')
		h3.cmd('nohup iperf3 -c 10.0.0.4 -u -b 1M -t 15 -p 5102 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_3_4.txt 2>&1 &')
		print('launching 4 -> 3 iperf')
		h4.cmd('nohup iperf3 -c 10.0.0.3 -u -b 1M -t 15 -p 5102 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_4_3.txt 2>&1 &')
		print('launching 3 -> 1 iperf')
		h3.cmd('nohup iperf3 -c 10.0.0.1 -u -b 1M -t 15 -p 5102 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_3_1.txt 2>&1 &')
		print('launching 4 -> 2 iperf')
		h4.cmd('nohup iperf3 -c 10.0.0.2 -u -b 1M -t 15 -p 5102 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_4_2.txt 2>&1 &')
		print('launching 1 -> 4 iperf')
		h1.cmd('nohup iperf3 -c 10.0.0.4 -u -b 1M -t 15 -p 5101 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_1_4.txt 2>&1 &')
		print('launching 2 -> 3 iperf')
		h2.cmd('nohup iperf3 -c 10.0.0.3 -u -b 1M -t 15 -p 5101 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_2_3.txt 2>&1 &')
		print('launching 3 -> 2 iperf')
		h3.cmd('nohup iperf3 -c 10.0.0.2 -u -b 1M -t 15 -p 5101 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_3_2.txt 2>&1 &')
		print('launching 4 -> 1 iperf')
		h4.cmd('nohup iperf3 -c 10.0.0.1 -u -b 1M -t 15 -p 5101 -i 1 > logs/2024-11-22-19:40:15.848572_4_4_4_1.txt 2>&1 &')
		
		# wait for iperf clients to finish
		print('wait for iperf clients to finish')
		time.sleep(30)
		
		# Kill iperf servers
		print('Kill iperf servers')
		h1.cmd('killall iperf3')
		h2.cmd('killall iperf3')
		h3.cmd('killall iperf3')
		h4.cmd('killall iperf3')
		
	except Exception as e:
		print(e)
