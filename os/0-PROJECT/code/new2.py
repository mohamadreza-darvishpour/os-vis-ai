def round_robin_scheduler(optimization_base, dl, process_arrival, process_burst_list):
    # Initialize variables
    max_burst = max(max(burst) for burst in process_burst_list if burst)
    n = len(process_arrival)
    
    best_quantum = 1
    best_metric = float('inf')
    best_gantt_chart = []
    
    for quantum in range(1, max_burst + 1):
        # Initialize per-simulation variables
        time = 0
        ready_queue = []
        io_queue = []
        completion_time = [-1] * n
        response_time = [-1] * n
        total_burst_time = [sum(burst[::2]) for burst in process_burst_list]  # CPU bursts only
        remaining_bursts = [burst[:] for burst in process_burst_list]  # Deep copy
        gantt_chart = []

        while True:
            # Add processes to the ready queue when they arrive
            for i in range(n):
                if process_arrival[i] <= time and remaining_bursts[i] and i not in ready_queue and i not in [p[0] for p in io_queue]:
                    ready_queue.append(i)

            # Handle CPU bursts
            if ready_queue:
                current_process = ready_queue.pop(0)
                if response_time[current_process] == -1:
                    response_time[current_process] = time - process_arrival[current_process]
                
                # Add dispatcher latency
                gantt_chart.append(("DL", dl))
                time += dl

                # Execute CPU burst
                execute_time = min(quantum, remaining_bursts[current_process][0])
                gantt_chart.append((f"P{current_process+1}", execute_time))
                time += execute_time
                remaining_bursts[current_process][0] -= execute_time

                # Check if CPU burst is completed
                if remaining_bursts[current_process][0] == 0:
                    remaining_bursts[current_process].pop(0)  # Remove the completed burst
                    if remaining_bursts[current_process]:
                        # Move to IO burst
                        io_burst_time = remaining_bursts[current_process].pop(0)
                        io_queue.append((current_process, time + io_burst_time))
                    else:
                        # Process is complete
                        completion_time[current_process] = time
                else:
                    # Re-add to ready queue
                    ready_queue.append(current_process)
            
            # Handle IO bursts
            io_queue = [(proc, end_time) for proc, end_time in io_queue if end_time > time]
            for proc, end_time in io_queue[:]:
                if end_time <= time:
                    ready_queue.append(proc)
                    io_queue.remove((proc, end_time))

            # Break when all processes are complete
            if all(not bursts for bursts in remaining_bursts) and not ready_queue and not io_queue:
                break

            # Advance time if nothing is ready
            if not ready_queue:
                gantt_chart.append(("Idle", 1))
                time += 1

        # Calculate metrics
        turnaround_time = [completion_time[i] - process_arrival[i] for i in range(n)]
        waiting_time = [turnaround_time[i] - total_burst_time[i] for i in range(n)]
        avg_turnaround_time = sum(turnaround_time) / n
        avg_waiting_time = sum(waiting_time) / n
        avg_response_time = sum(response_time) / n
        cpu_utilization = (sum(total_burst_time) / time) * 100

        # Select the best quantum based on the optimization base
        if optimization_base == 'w':
            metric = avg_waiting_time
        elif optimization_base == 't':
            metric = avg_turnaround_time
        elif optimization_base == 'r':
            metric = avg_response_time
        else:
            raise ValueError("Invalid optimization base. Use 'w', 't', or 'r'.")

        if metric < best_metric:
            best_metric = metric
            best_quantum = quantum
            best_gantt_chart = gantt_chart

    # Print results
    print(f"Best Quantum: {best_quantum}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Response Time: {avg_response_time:.2f}")
    print("Gantt Chart:")
    print(" -> ".join([f"[{process} for {duration}]" for process, duration in best_gantt_chart]))

    return {
        "best_quantum": best_quantum,
        "cpu_utilization": cpu_utilization,
        "avg_turnaround_time": avg_turnaround_time,
        "avg_waiting_time": avg_waiting_time,
        "avg_response_time": avg_response_time,
        "gant_chart": best_gantt_chart
    }


# Test case for the round robin scheduler

def test_round_robin():
    # Input data
    optimization_base = 'w'  # Optimize for waiting time
    dispatcher_latency = 2  # Dispatcher latency
    process_arrival = [0, 1, 2, 3]  # Arrival times for processes
    process_burst_list = [
        [4, 5, 3],  # Process 1: CPU burst, IO burst, CPU burst
        [3, 4, 2, 6],  # Process 2: CPU burst, IO burst, CPU burst, IO burst
        [5, 6],  # Process 3: CPU burst, IO burst
        [2]  # Process 4: CPU burst only
    ]

    # Call the round robin scheduler function
    result = round_robin_scheduler(optimization_base, dispatcher_latency, process_arrival, process_burst_list)

    # Print results
    print("\n===== Test Results =====")
    print("Best Quantum:", result['best_quantum'])
    print("CPU Utilization:", result['cpu_utilization'], "%")
    print("\ndic   : \n" , result)
    print("Average Turnaround Time:", result['avg_turnaround_time'])
    print("Average Waiting Time:", result['avg_waiting_time'])
    print("Average Response Time:", result['avg_response_time'])
    print("Gantt Chart:", result['gant_chart'])

# Run the test
test_round_robin()












