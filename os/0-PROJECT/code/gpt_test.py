import numpy as np 
from typing import List , Tuple 

# calculate turnaround time for all processess 
def calculate_turnaround_time(process_arrival: List[int] , completion_time:List[int]) -> List[int]:
    '''
    trunaround time = completion time - arrival time
    '''
    return [completion_time[i] - process_arrival[i]  for i in range(len(process_arrival))]


#calculating waiting time for all processes. 
def calculate_waiting_time(turnaround_time:List[int] , burst_sum:List[int]) -> List[int]:
    '''
    waiting time = turnarountime - total burst time
    '''
    return [turnaround_time[i]-burst_sum[i] for i in range(len(turnaround_time))]

#calculate response time
def calculate_response_time(response_start:List[int] , process_arrival:List[int])-> List[int]:
    '''
    response time = first response start time - arrival time 
    '''
    return [response_start[i] - process_arrival[i] for i in range(len(process_arrival))]


# RR simulator
def simulate_rr(
        quantum : int , 
        process_arrival: List[int ] , 
        process_burst_list: List[List[int]]
    ) -> Tuple[List[int] , List[int] , List[int] , int ]
    '''
    RR simulator.
    returns : 
    - completion_time: list of completion times for each process
    - response_start : list of first response time for each process
    -total burst : List of total burst times for each process
    -cpu_utilization : cpu utitlization percentage.
    '''
    n = len(process_arrival)
    ready_qeueu = []    # processes waiting for cpu
    io_qeueu  = []   #process performing io
    time = 0
    remaining_burst = [burst[0] if burst else 0 for burst in process_burst_list]
    burst_index = [0]*n  #tracks the current burst index of each process 
    completion_time = [-1]*n 
    response_start = [-1]*n  
    total_burst = [sum(burst[::2]) for burst in process_burst_list  ] #get the even index means all cpu burst index : 0 , 2 ,4 ,...
    
    
    while True:
    # add arriving processes to the ready qeueu 
        for i in range(n):
            if process_arrival[i] <= time and remaining_burst[i]>0 and i not in ready_qeueu :
                ready_qeueu.append(i)
                
        # handle cpu scheduling . 
        if ready_qeueu:
            current = ready_qeueu.pop(0)   #fetch the next process in the qeueu
            
            if response_start[current] == -1:
                response_start[current] = time   #record first response time 
            
            #execute for at most the quantum time or remaining burst time  
            executed_time = min(quantum , remaining_burst[current])
            time += executed_time 
            remaining_burst[current]  -= executed_time 
            
            #if burst ends switch ti io or complete process 
            if remaining_burst[current] == 0 : 
                burst_index[current] += 1 
                if burst_index[current] < len(process_burst_list[current]) :
                    #if there's an io burst , switch to io 
                    io_qeueu.append((current  , time + process_burst_list[current][burst_index[current]]))
                    burst_index[current] += 1 
                    if burst_index[current] < len(process_burst_list[current]):
                        remaining_burst[current] = process_burst_list[current][burst_index[current ]]
                else:
                    #process completed.
                    completion_time[current] = time 
            else:
                ready_qeueu.append(current)
        
        #handle io completion 
        for i, ( proc , io_end_time) in enumerate(io_qeueu):
            if io_end_time <= time :
                ready_qeueu.append(proc)
                io_qeueu.pop(i)
        
        # break condition : all processes are completed 
        if all(remaining_burst[i] == 0 for i in range(n)) and  not ready_qeueu and not io_qeueu : 
            break
        
        #advance time if no process is ready 
        if not  ready_qeueu:
            time += 1

    cpu_utilization = (sum(total_burst)/time) * 100
    return completion_time , response_start , total_burst , cpu_utilization
    

def optimize_quantum(
    optimization_base = str , 
    process_arrival: List[int] , 
    process_burst_list : List[List[int]] 
        )-> Tuple [int , dict]:
    '''
    test quantum from 1 to max cpu burst. 
    find best quantum based on ( w,r , t)
    return best quantum and performance metrics
    '''
    max_burst = max(max(burst[::2] , default=0) for burst in process_burst_list )
    best_quantum = 1
    best_metric = float('inf')
    performance = {} 
    
    for quantum in range(1 , max_burst+1) :
        completion_time , response_start , total_burst , cpu_utilization = simulate_rr(
            quantum=quantum , process_arrival= process_arrival , process_burst_list= process_burst_list
        )
        turnaround_time = calculate_turnaround_time(process_arrival , completion_time)
        waiting_time = calculate_waiting_time(turnaround_time , total_burst)
        response_time = calculate_response_time(response_start , process_arrival)
        
        
        
        