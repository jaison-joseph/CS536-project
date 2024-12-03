def run_tests(net):
    from datetime import datetime
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Get current timestamp for log files
    timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')


    # Get host objects
    h0, h1, h2, h3, h4, h5, h6, h7, h8, h9 = net.get('h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9')

    try:
        # start ditg servers
        h0.cmd('nohup ITGRecv &')
        h1.cmd('nohup ITGRecv &')
        h2.cmd('nohup ITGRecv &')
        h3.cmd('nohup ITGRecv &')
        h4.cmd('nohup ITGRecv &')
        h5.cmd('nohup ITGRecv &')
        h6.cmd('nohup ITGRecv &')
        h7.cmd('nohup ITGRecv &')
        h8.cmd('nohup ITGRecv &')
        h9.cmd('nohup ITGRecv &')
        
        # wait for servers to start
        time.sleep(5)
        
        # run iperf clients
        h0.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.47561 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_2 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.60025 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_3 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.12386 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_5 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.27591 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_8 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.27008 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_9 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.41705 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_5 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.82124 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_4 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.76854 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_7 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.78057 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_4 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.59796 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_5 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.91546 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_5 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.70953 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_0 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.76952 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_3 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.58871 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_4 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.15670 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_8 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.50561 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_0 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.99096 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_9 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.40943 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_1 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.97978 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_8 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.89561 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_0 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.10444 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_2 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.62804 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_3 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.49193 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_4 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.23027 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_0 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.44090 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_6 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.68359 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_7 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.19607 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_9 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.15825 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_2 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.51932 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_7 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.90410 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_1 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.13566 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_2 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.11534 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_7 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.62399 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_1 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.27434 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_9 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.08889 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_8 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.57667 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_8 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.71792 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_4 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.45623 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_3 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.81756 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_3 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.62404 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_6 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.29421 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_1 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.08910 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_2 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.96444 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_5 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.41095 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_9 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.15186 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_3 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.56645 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_7 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.29440 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_7 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.22008 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_1 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.54751 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_8 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.80772 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_4 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.91975 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_8 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.21310 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_2 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.42187 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_2 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.83054 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_5 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.16616 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_3 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.51076 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_3 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.16353 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_0 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.35073 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_5 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.61579 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_9 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.28678 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_0 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.20371 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_1 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.16124 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_2 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.09942 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_6 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.3 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.92707 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_2 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.76124 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_6 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.31171 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_4 2>&1 &')
        h0.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.28866 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_5 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.47246 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_4 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.01609 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_0 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.82052 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_0 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.92759 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_9 2>&1 &')
        h5.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.68019 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_1 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.1 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.47613 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_0 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.6 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.14544 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_5 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.84804 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_6 2>&1 &')
        h9.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.92658 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_8 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.34142 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_7 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.83048 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_9 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.56123 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_6 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.23639 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_1 2>&1 &')
        h8.cmd('nohup ITGSend -a 10.0.0.5 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.14335 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_4 2>&1 &')
        h2.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.20384 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_7 2>&1 &')
        h4.cmd('nohup ITGSend -a 10.0.0.2 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.19796 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_1 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.9 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.50012 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_8 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.10 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.76835 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_9 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.4 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.79094 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_3 2>&1 &')
        h6.cmd('nohup ITGSend -a 10.0.0.8 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.96908 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_7 2>&1 &')
        h1.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.24826 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_6 2>&1 &')
        h7.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 0.40680 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_6 2>&1 &')
        h3.cmd('nohup ITGSend -a 10.0.0.7 -T UDP -Fs cfg/ditg_packet_sizes.txt -E 1.12071 -t 90000 -x simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_6 2>&1 &')
        
        # wait for ITGSend to finish
        time.sleep(270)
        
        # Kill ITGRecv servers
        h0.cmd('killall ITGRecv')
        h1.cmd('killall ITGRecv')
        h2.cmd('killall ITGRecv')
        h3.cmd('killall ITGRecv')
        h4.cmd('killall ITGRecv')
        h5.cmd('killall ITGRecv')
        h6.cmd('killall ITGRecv')
        h7.cmd('killall ITGRecv')
        h8.cmd('killall ITGRecv')
        h9.cmd('killall ITGRecv')
        
        # wait for killing of ITGRecv processes
        time.sleep(10)
        
        # decode d-itg logs to 10-second interval stats
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_2')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_3')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_5')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_8')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_9')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_5')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_4')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_7')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_4')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_5')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_5')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_0')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_3')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_4')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_8')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_0')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_9')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_1')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_8')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_0')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_2')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_3')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_4')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_0')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_6')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_7')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_9')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_2')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_7')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_1')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_2')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_7')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_1')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_9')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_8')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_8')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_4')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_3')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_3')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_6')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_1')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_2')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_5')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_9')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_3')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_7')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_7')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_1')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_8')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_4')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_8')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_2')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_2')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_5')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_3')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_3')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_0')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_5')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_9')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_0')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_1')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_2')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_6')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_2 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_2')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_6')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_4')
        h0.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_0_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_0_5')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_4')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_0')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_0')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_9')
        h5.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_5_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_5_1')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_0 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_0')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_5 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_5')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_6')
        h9.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_9_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_9_8')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_7')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_9')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_6')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_1')
        h8.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_8_4 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_8_4')
        h2.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_2_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_2_7')
        h4.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_4_1 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_4_1')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_8 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_8')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_9 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_9')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_3 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_3')
        h6.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_6_7 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_6_7')
        h1.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_1_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_1_6')
        h7.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_7_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_7_6')
        h3.cmd('ITGDec simulations/nsfnet_10_9_11/lambda_10/run_2/raw_data/2024-12-03-21:16:31.397634_10_10_3_6 -c 1000 simulations/nsfnet_10_9_11/lambda_10/run_2/decoded_data/2024-12-03-21:16:31.397634_10_10_3_6')
        
    except Exception as e:
        return 1

# this file is executed from the mininet shell; this is how to use it:
# mininet> py execfile('test.py')
# mininet> py run_tests(net)
