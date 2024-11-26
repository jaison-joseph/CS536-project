def run_tests(net):
	from datetime import datetime
	# Create logs directory if it doesn't exist
	if not os.path.exists('logs'):
		os.makedirs('logs')

	# Get current timestamp for log files
	timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')


	# Get host objects
	h0, h1, h2, h3 = net.get('h0', 'h1', 'h2', 'h3')

	try:
		# start ditg servers
		print('starting ditg server @ 0')
		h0.cmd('nohup ITGRecv &')
		print('starting ditg server @ 1')
		h1.cmd('nohup ITGRecv &')
		print('starting ditg server @ 2')
		h2.cmd('nohup ITGRecv &')
		print('starting ditg server @ 3')
		h3.cmd('nohup ITGRecv &')
		
		# wait for servers to start
		print('wait for servers to start')
		time.sleep(2)
		
		# run iperf clients
		print('run iperf clients')
		print('launching 0 -> 1 ITGSend')
		h0.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 2.70984 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_0_1.txt 2>&1 &')
		print('launching 1 -> 2 ITGSend')
		h1.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 3.22250 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_1_2.txt 2>&1 &')
		print('launching 2 -> 0 ITGSend')
		h2.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 0.52373 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_2_0.txt 2>&1 &')
		print('launching 1 -> 3 ITGSend')
		h1.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 1.16544 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_1_3.txt 2>&1 &')
		print('launching 2 -> 1 ITGSend')
		h2.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 2.96090 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_2_1.txt 2>&1 &')
		print('launching 1 -> 0 ITGSend')
		h1.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 2.79867 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_1_0.txt 2>&1 &')
		print('launching 3 -> 2 ITGSend')
		h3.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 2.31692 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_3_2.txt 2>&1 &')
		print('launching 0 -> 2 ITGSend')
		h0.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 1.38556 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_0_2.txt 2>&1 &')
		print('launching 3 -> 1 ITGSend')
		h3.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 3.11946 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_3_1.txt 2>&1 &')
		print('launching 2 -> 3 ITGSend')
		h2.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 1.01068 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_2_3.txt 2>&1 &')
		print('launching 3 -> 0 ITGSend')
		h3.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 3.38893 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_3_0.txt 2>&1 &')
		print('launching 0 -> 3 ITGSend')
		h0.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -C 2.66301 -t 15000 -x logs/2024-11-26-08:01:04.345364_0_0_0_3.txt 2>&1 &')
		
		# wait for ITGSend to finish
		print('wait for ITGSend to finish')
		time.sleep(30)
		
		# Kill ITGRecv servers
		print('Kill ITGRecv servers')
		h0.cmd('killall ITGRecv')
		h1.cmd('killall ITGRecv')
		h2.cmd('killall ITGRecv')
		h3.cmd('killall ITGRecv')
		
	except Exception as e:
		print(e)

# this file is executed from the mininet shell; this is how to use it:
# mininet> py execfile('test.py')
# mininet> py run_tests(net)
