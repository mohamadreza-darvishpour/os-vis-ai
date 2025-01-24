from in_out_func import make_out_file , lines_of_input_file , lines_to_dict 
from best_rr import round_robin_scheduler 




import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python my_code.py <input_file>")
        sys.exit(1)


    '''
    input is list ; example : 
        [['W'], [68], ['p1:6', 8, 9, 19, 29, 39], ['p2:9', 8, 9, 19], ['p3:6', 8, 9, 19, 29, 39], ['p4:9', 8, 9, 19], ['p5:6', 8, 9, 19, 29, 39]]
    
    output is dict , example : 
        {'opt_base': 'W', 
        'dl': 68, 
        'process_arrival': [6, 9, 6, 9, 6], 
        'burst_list': [[8, 9, 19, 29, 39], [8, 9, 19], [8, 9, 19, 29, 39], [8, 9, 19], [8, 9, 19, 29, 39]]}
    '''

    input_file_path = sys.argv[1]        #input file path
    data_dict = lines_to_dict(lines_of_input_file(input_file_path))
    # print(data_dict)
    res =   round_robin_scheduler(
        optimization_base= data_dict[ 'opt_base' ].lower() ,
        dl= data_dict[ 'dl' ]   , 
        process_arrival=  data_dict[ 'process_arrival' ]   , 
        processes_burst_lists= data_dict[ 'burst_list' ]   , 
    )
    # print(res)
    # make_out_file(res)
    # print('\n\n\nresult : ' , result  )
    string = '' 
    for key , val in res.items():
        string += f'{key} : {val} \n'
    make_out_file(string)


'''
 data_dict = {
        'opt_base' : file_lines_list[0][0] , 
        'dl'       : file_lines_list[1][0] , 
        'process_arrival' : process_arrival,
        'burst_list'   :   burst_list   ,
    }

'''


if __name__ == "__main__":
    main()













