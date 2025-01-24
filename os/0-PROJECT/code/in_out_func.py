
#imports
import numpy as np
from typing import List, Tuple
import sys


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
                        'W' in cleaned[x][y] or 
                        'T' in cleaned[x][y] or 
                        't' in cleaned[x][y]  
                        
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
        'opt_base' : file_lines_list[0][0].lower() , 
        'dl'       : file_lines_list[1][0] , 
        'process_arrival' : process_arrival,
        'burst_list'   :   burst_list   ,
    }
    return data_dict


# writing output file 
def make_out_file(text:str):
    # try :
        file_name = 'output.txt'

        with open(f'{file_name}', 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"\nFile '{file_name}' created successfully with content: {text}\n")

    # except Exception as e : 
    #     print(f'\nerror making output file. \n')




