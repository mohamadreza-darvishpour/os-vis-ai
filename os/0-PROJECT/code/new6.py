







def round_robin_scheduler(optimization_base, dl, process_arrival, processes_burst_lists):
    # Find the maximum burst time to determine the range for quantum
    max_burst = max(max(bursts) for bursts in processes_burst_lists if bursts)
    best_quantum = 1
    best_metrics = None
    best_gantt_chart = []  # Track the best Gantt chart

    # Try all possible quantum values from 1 to max_burst
    for quantum in range(1, max_burst + 1):
        print(f"\nTesting quantum = {quantum}")
        ready_queue = []
        io_queue = []
        current_time = 0
        processes = list(range(len(process_arrival)))  # List of active processes
        arrival_times = process_arrival[:]
        burst_times = [bursts[:] for bursts in processes_burst_lists]
        completion_times = [-1] * len(process_arrival)  # Initialize completion times
        first_response = [-1] * len(process_arrival)  # Initialize first response times
        total_cpu_busy_time = 0  # Track total CPU busy time
        total_elapsed_time = 0  # Track total elapsed time
        gantt_chart = []  # Track the Gantt chart for this quantum

        while processes or ready_queue or io_queue:
            # Add arriving processes to the ready queue
            for i in processes[:]:
                if arrival_times[i] <= current_time and i not in ready_queue:
                    ready_queue.append(i)
                    processes.remove(i)

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
            if first_response[process] == -1:
                first_response[process] = current_time

            # Execute the process for the quantum or remaining burst time
            if burst_times[process]:
                burst = burst_times[process].pop(0)
                executed_time = min(burst, quantum)
                total_cpu_busy_time += executed_time  # Add to total CPU busy time
                gantt_chart.append((process, current_time, current_time + executed_time))  # Add to Gantt chart
                current_time += executed_time

                if burst > quantum:
                    burst_times[process].insert(0, burst - quantum)
                    ready_queue.append(process)
                elif burst_times[process]:
                    io_burst = burst_times[process].pop(0)
                    io_queue.append((process, current_time + io_burst))
                else:
                    # Process has completed all bursts
                    completion_times[process] = current_time

            # Add dispatcher latency
            current_time += dl

        # Calculate total elapsed time
        total_elapsed_time = current_time

        # Debug prints for CPU utilization calculation
        print(f"Total CPU Busy Time: {total_cpu_busy_time}")
        print(f"Total Elapsed Time: {total_elapsed_time}")

        # Calculate CPU utilization
        if total_elapsed_time > 0:
            cpu_utilization = (total_cpu_busy_time / total_elapsed_time) * 100
        else:
            cpu_utilization = 0

        # Calculate turnaround, waiting, and response times
        n = len(process_arrival)
        turnaround_times = [completion_times[i] - arrival_times[i] for i in range(n)]
        waiting_times = [turnaround_times[i] - sum(processes_burst_lists[i]) for i in range(n)]
        response_times = [first_response[i] - arrival_times[i] for i in range(n)]

        avg_turnaround_time = sum(turnaround_times) / n
        avg_waiting_time = sum(waiting_times) / n
        avg_response_time = sum(response_times) / n

        metrics = {
            "avg_turnaround_time": avg_turnaround_time,
            "avg_waiting_time": avg_waiting_time,
            "avg_response_time": avg_response_time,
            "cpu_utilization": cpu_utilization,
        }

        # Debug prints for metrics
        print(f"CPU Utilization: {cpu_utilization}%")
        print(f"Average Turnaround Time: {avg_turnaround_time}")
        print(f"Average Response Time: {avg_response_time}")
        print(f"Average Waiting Time: {avg_waiting_time}")

        # Check if this quantum is better based on optimization_base
        if (
            (optimization_base == "W" and (not best_metrics or metrics["avg_waiting_time"] < best_metrics["avg_waiting_time"]))
            or (optimization_base == "R" and (not best_metrics or metrics["avg_response_time"] < best_metrics["avg_response_time"]))
            or (optimization_base == "T" and (not best_metrics or metrics["avg_turnaround_time"] < best_metrics["avg_turnaround_time"]))
        ):
            best_quantum = quantum
            best_metrics = metrics
            best_gantt_chart = gantt_chart  # Update the best Gantt chart

    # Output the results
    print("\nFinal Results:")
    print("Best Quantum:", best_quantum)
    print("CPU Utilization:", best_metrics["cpu_utilization"], "%")
    print("Average Turnaround Time:", best_metrics["avg_turnaround_time"])
    print("Average Response Time:", best_metrics["avg_response_time"])
    print("Average Waiting Time:", best_metrics["avg_waiting_time"])
    print("Best Gantt Chart:", best_gantt_chart)

    return {
        "cpu_utilization": best_metrics["cpu_utilization"],
        "avg_turnaround_time": best_metrics["avg_turnaround_time"],
        "avg_response_time": best_metrics["avg_response_time"],
        "avg_waiting_time": best_metrics["avg_waiting_time"],
        "best_gantt_chart": best_gantt_chart,  # Include the best Gantt chart in the results
    }


# Test the function
optimization_base = "T"  # 'W' for waiting time, 'R' for response time, 'T' for turnaround time
dl = 1  # Dispatcher latency
process_arrival = [0, 1,3,3, 2, 3]
processes_burst_lists = [
    [3, 10, 1, 30 , 9],
    [1, 12, 1, 1, 1],
    [1, 12, 1, 1, 1],
    [1, 12, 1, 1, 1],
    [1, 2],
    [1],
]

result = round_robin_scheduler(optimization_base, dl, process_arrival, processes_burst_lists)