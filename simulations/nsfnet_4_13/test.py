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
        h0.cmd('nohup ITGRecv &')
        h1.cmd('nohup ITGRecv &')
        h2.cmd('nohup ITGRecv &')
        h3.cmd('nohup ITGRecv &')
        
        # wait for servers to start
        time.sleep(2)
        
        # run iperf clients
        h1.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.56583 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_1_3 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.88174 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_0_3 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.81626 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_1_2 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.32693 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_2_1 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.60630 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_3_0 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.59847 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_0_2 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.89063 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_0_1 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.42758 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_3_2 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.94303 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_2_0 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.21143 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_2_3 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 2.44272 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_1_0 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.75965 -t 30000 -x simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_3_1 2>&1 &')
        
        # wait for ITGSend to finish
        time.sleep(39)
        
        # Kill ITGRecv servers
        h0.cmd('killall ITGRecv')
        h1.cmd('killall ITGRecv')
        h2.cmd('killall ITGRecv')
        h3.cmd('killall ITGRecv')
        
        # wait for killing of ITGRecv processes
        time.sleep(2)
        
        # decode d-itg logs to 10-second interval stats
        h1.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_1_3 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_1_3')
        h0.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_0_3 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_0_3')
        h1.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_1_2 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_1_2')
        h2.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_2_1 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_2_1')
        h3.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_3_0 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_3_0')
        h0.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_0_2 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_0_2')
        h0.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_0_1 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_0_1')
        h3.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_3_2 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_3_2')
        h2.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_2_0 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_2_0')
        h2.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_2_3 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_2_3')
        h1.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_1_0 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_1_0')
        h3.cmd('ITGDec simulations/nsfnet_4_13/run_3/raw_data/2024-11-29-17:40:45.458322_4_4_3_1 -c 1000 simulations/nsfnet_4_13/run_3/decoded_data/2024-11-29-17:40:45.458322_4_4_3_1')
        
    except Exception as e:
        return 1

# this file is executed from the mininet shell; this is how to use it:
# mininet> py execfile('test.py')
# mininet> py run_tests(net)
