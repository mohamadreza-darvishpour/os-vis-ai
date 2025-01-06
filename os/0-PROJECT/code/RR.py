'''
input file structure 
line_1 >W    # W or R or T    which should be optimized? 
line_2 >68   #dl : dispatcher latency

LIne_3 >p1 : arrival_time , cpu_burst ,i_o_burst , cpu_burst , i_o_burst , cpu_burst ,........   # no specific amount.
line_4 >p2:6 , 8 ,9,19,29,39,........
line_5 > ....
...
...
line_N >pN:8 , 9 ,19 ,............     # N.th process.   not specific amount: N . 

'''

#####   output 
'''
2     #optimized quantom.
________________________________________________________
p7|p8|p9|p2|w |p1|p2|
______________________________________

'''











test_path  = './code/test.txt'
test_dict = {1:'red' , 2:'blue' , 3:'black'}
#imports
import numpy as np
from typing import List, Tuple



# cleaning the lines of the input file and return list of lines. 
def lines_of_input_file(file_path):
    '''get the input file path and return list of object like: 
    [['W'], ['68'], ['p2:6', '8', '9', '19', '29', '39'], ['p2:9', '8', '9', '19'], ['p2:6', '8', '9', '19', '29', '39']]
    '''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for index in range(len(lines)):
                lines[index]  = (lines[index].strip().replace(' ' ,'').replace(',',' ').strip().split())
        cleaned = [item for item in lines if len(item) !=0]
        for x in range(len(cleaned)): 
            for y in range(len(cleaned[x])) : 
                if( not( 
                        'p' in cleaned[x][y] or
                        'P' in cleaned[x][y] or
                        'w' in cleaned[x][y] or
                        'W' in cleaned[x][y] 
                        )):
                    cleaned[x][y] = int(cleaned[x][y])
                
        # print('\ncleaned : ', cleaned , '\n')
        return  cleaned

    except FileNotFoundError:
        print(f"\nError: The file at {file_path} was not found.\n")
        return''
    except Exception as e:
        print(f"\nError reading file: {e}\n")
        return''


# make list of object get from input lines list 
def lines_to_dict(file_lines_list:list) -> dict :
    '''
    input is list ; example : 
        [['W'], [68], ['p1:6', 8, 9, 19, 29, 39], ['p2:9', 8, 9, 19], ['p3:6', 8, 9, 19, 29, 39], ['p4:9', 8, 9, 19], ['p5:6', 8, 9, 19, 29, 39]]
    
    output is dict , example : 
        {'opt_base': 'W', 
        'dl': 68, 
        'process_arrival': [6, 9, 6, 9, 6], 
        'burst_list': [[8, 9, 19, 29, 39], [8, 9, 19], [8, 9, 19, 29, 39], [8, 9, 19], [8, 9, 19, 29, 39]]}
    '''
    # handle process arrrival
    process_arrival = [ file_lines_list[i][0] for i in range(2 , len(file_lines_list)) ]
    for ind in range(len(process_arrival)):
        item = process_arrival[ind]
        item = int(item.split(':')[1])
        # item = int(item.replace('p' , '').replace('P', ''))
        process_arrival[ind ]  = item
    #   <<<  end >>> of handle process arrival    
    burst_list = [ proc_bursts[1:] for proc_bursts in file_lines_list[2:]]
    
    data_dict = {
        'opt_base' : file_lines_list[0][0] , 
        'dl'       : file_lines_list[1][0] , 
        'process_arrival' : process_arrival,
        'burst_list'   :   burst_list   ,
    }
    return data_dict


# writing output file 
def make_out_file(p_col_dict:dict):
    # try :
        result = ''
        file_name = 'output.txt'

        with open(f'./code/{file_name}', 'w', encoding='utf-8') as file:
            file.write(result)
        print(f"\nFile '{file_name}' created successfully with content: {result}\n")

    # except Exception as e : 
    #     print(f'\nerror making output file. \n')







# Function to calculate turnaround time for all processes
def calculate_turnaround_time(process_arrival: List[int], completion_time: List[int]) -> List[int]:
    """
    Turnaround Time = Completion Time - Arrival Time
    """
    return [completion_time[i] - process_arrival[i] for i in range(len(process_arrival))]

# Function to calculate waiting time for all processes
def calculate_waiting_time(turnaround_time: List[int], burst_sum: List[int]) -> List[int]:
    """
    Waiting Time = Turnaround Time - Total Burst Time
    """
    return [turnaround_time[i] - burst_sum[i] for i in range(len(turnaround_time))]

# Function to calculate response time for all processes
def calculate_response_time(response_start: List[int], process_arrival: List[int]) -> List[int]:
    """
    Response Time = First Response Start Time - Arrival Time
    """
    return [response_start[i] - process_arrival[i] for i in range(len(process_arrival))]

# Function to simulate round-robin scheduling
def simulate_rr(
    quantum: int,
    process_arrival: List[int],
    process_burst_list: List[List[int]],
    dl: int
) -> Tuple[List[int], List[int], List[int], int, List[Tuple[str, int]]]:
    """
    Simulate the round-robin scheduling with dispatcher latency.
    Returns:
    - completion_time: List of completion times for each process
    - response_start: List of first response times for each process
    - total_burst: List of total burst times for each process
    - cpu_utilization: CPU utilization percentage
    - gantt_chart: List of tuples representing the Gantt chart (process name, execution time)
    """
    n = len(process_arrival)
    ready_queue = []  # Holds processes waiting for CPU
    io_queue = []  # Holds processes performing IO
    time = 0
    remaining_burst = [burst[0] if burst else 0 for burst in process_burst_list]
    burst_index = [0] * n  # Tracks the current burst index of each process
    completion_time = [-1] * n
    response_start = [-1] * n
    total_burst = [sum(burst[::2]) for burst in process_burst_list]  # Sum of CPU bursts only
    gantt_chart = []

    while True:
        # Add arriving processes to the ready queue
        for i in range(n):
            if process_arrival[i] <= time and remaining_burst[i] > 0 and i not in ready_queue:
                ready_queue.append(i)

        # Handle CPU scheduling
        if ready_queue:
            current = ready_queue.pop(0)  # Fetch the next process in the queue

            # Add dispatcher latency for context switch
            gantt_chart.append(("DL", dl))
            time += dl

            if response_start[current] == -1:
                response_start[current] = time  # Record first response time

            # Execute for at most the quantum time or remaining burst time
            executed_time = min(quantum, remaining_burst[current])
            gantt_chart.append((f"P{current + 1}", executed_time))
            time += executed_time
            remaining_burst[current] -= executed_time

            # If burst ends, switch to IO or complete process
            if remaining_burst[current] == 0:
                burst_index[current] += 1
                if burst_index[current] < len(process_burst_list[current]):
                    # If there's an IO burst, switch to IO
                    io_queue.append((current, time + process_burst_list[current][burst_index[current]]))
                    burst_index[current] += 1
                    if burst_index[current] < len(process_burst_list[current]):
                        remaining_burst[current] = process_burst_list[current][burst_index[current]]
                else:
                    # Process completed
                    completion_time[current] = time
            else:
                ready_queue.append(current)  # Re-add to the ready queue if not finished

        # Handle IO completion
        for i, (proc, io_end_time) in enumerate(io_queue):
            if io_end_time <= time:
                ready_queue.append(proc)
                io_queue.pop(i)

        # Break condition: All processes are completed
        if all(remaining_burst[i] == 0 for i in range(n)) and not ready_queue and not io_queue:
            break

        # Advance time if no process is ready
        if not ready_queue:
            gantt_chart.append(("Idle", 1))
            time += 1

    cpu_utilization = (sum(total_burst) / time) * 100
    return completion_time, response_start, total_burst, cpu_utilization, gantt_chart

# Function to optimize quantum based on the chosen metric
def optimize_quantum(
    optimization_base: str,
    process_arrival: List[int],
    process_burst_list: List[List[int]],
    dl: int
) -> Tuple[int, dict, List[Tuple[str, int]]]:
    """
    Test quantum values from 1 to max CPU burst and find the best quantum
    based on the selected optimization base ('w', 't', 'r').
    Returns the best quantum and the performance metrics.
    """
    max_burst = max(max(burst[::2], default=0) for burst in process_burst_list)
    best_quantum = 1
    best_metric = float('inf')
    performance = {}
    best_gantt_chart = []

    for quantum in range(1, max_burst + 1):
        completion_time, response_start, total_burst, cpu_utilization, gantt_chart = simulate_rr(
            quantum, process_arrival, process_burst_list, dl
        )

        turnaround_time = calculate_turnaround_time(process_arrival, completion_time)
        waiting_time = calculate_waiting_time(turnaround_time, total_burst)
        response_time = calculate_response_time(response_start, process_arrival)

        avg_turnaround = np.mean(turnaround_time)
        avg_waiting = np.mean(waiting_time)
        avg_response = np.mean(response_time)

        if optimization_base == 'w':
            metric = avg_waiting
        elif optimization_base == 't':
            metric = avg_turnaround
        elif optimization_base == 'r':
            metric = avg_response
        else:
            raise ValueError("Invalid optimization base. Use 'w', 't', or 'r'.")

        if metric < best_metric:
            best_metric = metric
            best_quantum = quantum
            best_gantt_chart = gantt_chart

        performance[quantum] = {
            'avg_turnaround_time': avg_turnaround,
            'avg_waiting_time': avg_waiting,
            'avg_response_time': avg_response,
            'cpu_utilization': cpu_utilization
        }

    return best_quantum, performance[best_quantum], best_gantt_chart
 
# Function to print the Gantt chart
def print_gantt_chart(gantt_chart: List[Tuple[str, int]]) -> None:
    """
    Prints the Gantt chart in a human-readable format.
    """
    print("Gantt Chart:")
    for process, duration in gantt_chart:
        print(f"[{process} for {duration} units]", end=" -> ")
    print("End")






proc_list = lines_of_input_file(test_path)
print(lines_to_dict(proc_list))



























