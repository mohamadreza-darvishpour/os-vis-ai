def round_robin_scheduler(optimization_base, dl, process_arrival, processes_burst_lists):
    # Find the maximum burst time to determine the range for quantum
    max_burst = 0
    for bursts in processes_burst_lists:
        if bursts:
            current_max = max(bursts)
            if current_max > max_burst:
                max_burst = current_max

    best_quantum = 1
    best_metrics = None
    best_gantt_chart = []

    # Try all possible quantum values from 1 to max_burst
    for quantum in range(1, max_burst + 1):
        print(f"Testing quantum = {quantum}")
        gantt_chart = []
        ready_queue = []  # Simple list for queue operations
        io_queue = []
        current_time = 0
        processes = list(range(len(process_arrival)))  # List of active processes
        arrival_times = process_arrival.copy()
        burst_times = [bursts.copy() for bursts in processes_burst_lists]
        completion_times = [0] * len(processes)
        first_response = [0] * len(processes)
        remaining_bursts = [sum(bursts) for bursts in burst_times]
        count1 = 0 
        while count1<50 and processes:
            count1 += 1 
            # Debugging: Print current state
            print(f"c_{count1}: Time = {current_time}, Ready Queue = {ready_queue}, IO Queue = {io_queue}, Processes = {processes}")

            # Add arriving processes to the ready queue
            for i in processes:
                if arrival_times[i] <= current_time and i not in ready_queue:
                    # Check if the process is not in the IO queue
                    in_io_queue = False
                    for p in io_queue:
                        if p[0] == i:
                            in_io_queue = True
                            break
                    if not in_io_queue:
                        ready_queue.append(i)

            # Handle IO bursts
            i = 0
            while i < len(io_queue):
                process, io_time = io_queue[i]
                if io_time <= current_time:
                    ready_queue.append(process)
                    io_queue.pop(i)
                else:
                    i += 1

            # If no processes are ready to run, increment time
            if not ready_queue:
                current_time += 1
                continue

            # Get the next process from the ready queue
            process = ready_queue.pop(0)

            # Record response time if it's the first time the process is executed
            if first_response[process] == 0:
                first_response[process] = current_time

            # Execute the process for the quantum or remaining burst time
            if len(burst_times[process]) > 0:
                burst = burst_times[process].pop(0)
                if burst > quantum:
                    gantt_chart.append((process, current_time, current_time + quantum))
                    current_time += quantum
                    burst_times[process].insert(0, burst - quantum)
                    ready_queue.append(process)
                else:
                    gantt_chart.append((process, current_time, current_time + burst))
                    current_time += burst
                    if len(burst_times[process]) > 0:
                        io_burst = burst_times[process].pop(0)
                        io_queue.append((process, current_time + io_burst))
                    else:
                        # Process has completed all bursts
                        completion_times[process] = current_time
                        processes.remove(process)  # Remove the process from the active list

            # Add dispatcher latency
            current_time += dl

            # Check if all processes have completed
            if not processes:
                break  # Exit the loop if no processes are left

        # Calculate metrics
        n = len(process_arrival)
        turnaround_times = [completion_times[i] - arrival_times[i] for i in range(n)]
        waiting_times = [turnaround_times[i] - sum(processes_burst_lists[i]) for i in range(n)]
        response_times = [first_response[i] - arrival_times[i] for i in range(n)]
        
        avg_turnaround_time = sum(turnaround_times) / n
        avg_waiting_time = sum(waiting_times) / n
        avg_response_time = sum(response_times) / n
        cpu_utilization = (sum(sum(bursts) for bursts in processes_burst_lists) / completion_times[-1]) * 100

        metrics = {
            "avg_turnaround_time": avg_turnaround_time,
            "avg_waiting_time": avg_waiting_time,
            "avg_response_time": avg_response_time,
            "cpu_utilization": cpu_utilization,
        }

        # Check if this quantum is better based on optimization_base
        if optimization_base == 'W' and (best_metrics is None or metrics["avg_waiting_time"] < best_metrics["avg_waiting_time"]):
            best_quantum = quantum
            best_metrics = metrics
            best_gantt_chart = gantt_chart
        elif optimization_base == 'R' and (best_metrics is None or metrics["avg_response_time"] < best_metrics["avg_response_time"]):
            best_quantum = quantum
            best_metrics = metrics
            best_gantt_chart = gantt_chart
        elif optimization_base == 'T' and (best_metrics is None or metrics["avg_turnaround_time"] < best_metrics["avg_turnaround_time"]):
            best_quantum = quantum
            best_metrics = metrics
            best_gantt_chart = gantt_chart

    # Output the results
    print("Gantt Chart:", best_gantt_chart)
    print("CPU Utilization:", best_metrics["cpu_utilization"], "%")
    print("Average Turnaround Time:", best_metrics["avg_turnaround_time"])
    print("Average Response Time:", best_metrics["avg_response_time"])
    print("Average Waiting Time:", best_metrics["avg_waiting_time"])
    print("best_quantum: " ,  best_quantum )

    return {
        "gantt_chart": best_gantt_chart,
        "cpu_utilization": best_metrics["cpu_utilization"],
        "avg_turnaround_time": best_metrics["avg_turnaround_time"],
        "avg_response_time": best_metrics["avg_response_time"],
        "avg_waiting_time": best_metrics["avg_waiting_time"],
    }


# Test the function
optimization_base = 'W'  # 'W' for waiting time, 'R' for response time, 'T' for turnaround time
dl = 1  # Dispatcher latency
process_arrival = [6, 2, 2, 3]
processes_burst_lists = [
    [3, 10, 1], 
    [1, 12, 1, 1, 1], 
    [1,2], 
    [1]
    ]

result = round_robin_scheduler(optimization_base, dl, process_arrival, processes_burst_lists)