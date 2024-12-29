'''
input file structure 
line_1 >W    # W or R or T    which should be optimized? 
line_2 >68   #dl : datalatency

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




def lines_of_input_file(file_path):
    '''get the input file path and return (numpy) matris'''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for index in range(len(lines)):
                lines[index]  = lines[index].strip().split(',')
        return lines

    except FileNotFoundError:
        print(f"\nError: The file at {file_path} was not found.\n")
        return''
    except Exception as e:
        print(f"\nError reading file: {e}\n")
        return''


def make_out_file(p_col_dict:dict):
    # try :
        result = ''
        file_name = 'output.txt'
        for key , color in p_col_dict.items():
            result += f'{key}={color},'
        with open(f'./code/{file_name}', 'w', encoding='utf-8') as file:
            file.write(result)
        print(f"\nFile '{file_name}' created successfully with content: {result}\n")

    # except Exception as e : 
    #     print(f'\nerror making output file. \n')







print(lines_of_input_file(test_path))
# make_out_file(test_dict)


























