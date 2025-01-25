def round_robin_scheduler(optimization_base, dl, process_arrival, processes_burst_lists):
    """
    A Round Robin Scheduler with dispatcher latency applied for both CPU and I/O bursts.
    """
    max_burst = max(max(bursts) for bursts in processes_burst_lists if bursts)
    best_quantum = 1
    best_metrics = None
    best_gantt_chart = []

    for quantum in range(1, max_burst + 1):
        ready_queue = []
        io_queue = []
        current_time = 0
        processes = list(range(len(process_arrival)))
        arrival_times = process_arrival[:]
        burst_times = [bursts[:] for bursts in processes_burst_lists]
        completion_times = [-1] * len(process_arrival)
        first_response = [-1] * len(process_arrival)
        total_cpu_busy_time = 0
        gantt_chart = []

        while processes or ready_queue or io_queue:
            # Add arriving processes to the ready queue
            for i in processes[:]:
                if arrival_times[i] <= current_time and i not in ready_queue:
                    ready_queue.append(i)
                    processes.remove(i)

            # Handle I/O bursts
            i = 0
            while i < len(io_queue):
                process, io_time = io_queue[i]
                if io_time <= current_time:
                    # Add dispatcher latency for I/O return
                    current_time += dl
                    ready_queue.append(process)
                    io_queue.pop(i)
                else:
                    i += 1

            # Increment time if no processes are ready
            if not ready_queue:
                current_time += 1
                continue

            # Get the next process from the ready queue
            process = ready_queue.pop(0)

            # Record response time
            if first_response[process] == -1:
                first_response[process] = current_time

            # Execute the process for quantum or remaining burst
            if burst_times[process]:
                burst = burst_times[process].pop(0)
                executed_time = min(burst, quantum)
                total_cpu_busy_time += executed_time
                gantt_chart.append((process, current_time, current_time + executed_time))
                current_time += executed_time

                if burst > quantum:
                    burst_times[process].insert(0, burst - quantum)
                    ready_queue.append(process)
                elif burst_times[process]:
                    io_burst = burst_times[process].pop(0)
                    io_queue.append((process, current_time + io_burst))
                else:
                    completion_times[process] = current_time

            # Add dispatcher latency after CPU burst
            current_time += dl

        # Calculate metrics
        total_elapsed_time = current_time
        cpu_utilization = (total_cpu_busy_time / total_elapsed_time) * 100 if total_elapsed_time > 0 else 0

        n = len(process_arrival)
        turnaround_times = [
            max(completion_times[i] - arrival_times[i], 0) for i in range(n)
        ]
        waiting_times = [
            max(turnaround_times[i] - sum(processes_burst_lists[i]), 0) for i in range(n)
        ]
        response_times = [
            max(first_response[i] - arrival_times[i], 0) for i in range(n)
        ]
        avg_turnaround_time = sum(turnaround_times) / n
        avg_waiting_time = sum(waiting_times) / n
        avg_response_time = sum(response_times) / n

        metrics = {
            "avg_turnaround_time": avg_turnaround_time,
            "avg_waiting_time": avg_waiting_time,
            "avg_response_time": avg_response_time,
            "cpu_utilization": cpu_utilization,
        }

        # Optimize based on the selected metric
        if (
            (optimization_base in "wW" and (not best_metrics or metrics["avg_waiting_time"] < best_metrics["avg_waiting_time"]))
            or (optimization_base in "rR" and (not best_metrics or metrics["avg_response_time"] < best_metrics["avg_response_time"]))
            or (optimization_base in "Tt" and (not best_metrics or metrics["avg_turnaround_time"] < best_metrics["avg_turnaround_time"]))
        ):
            best_quantum = quantum
            best_metrics = metrics
            best_gantt_chart = gantt_chart

    return {
        "best_quantum": best_quantum,
        "avg_turnaround_time": best_metrics["avg_turnaround_time"],
        "cpu_utilization": best_metrics["cpu_utilization"],
        "avg_response_time": best_metrics["avg_response_time"],
        "avg_waiting_time": best_metrics["avg_waiting_time"],
        "best_gantt_chart": best_gantt_chart,
    }
