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



class RR:
    def __init__(self , process_list:list):
        self.p_num = 0          #process amount
        self.data_dict = {}
        self.data_dict['processes'] = {}
        for ind in range(len(process_list)):
            if(ind == 0):
                self.data_dict['opt_base'] = process_list[ind][0]   #given amount base to use in order to optimize.(w-r-t)
            elif (ind == 1):
                self.data_dict['dl'] = int(process_list[ind][0])     # given dispatcher latency #int may be got problem.
            else:
                self.p_num +=1 
                proc_number = int((process_list[ind][0].replace('p','').split(':'))[0]  )   #process number
                proc_arrive = int((process_list[ind][0].replace('p','').split(':'))[1] )    #process arrival
                del process_list[ind][0]
                self.data_dict['processes'][proc_number] = {
                    'bursts' :    process_list[ind] ,
                    'arrive' : proc_arrive ,
                }
                # for p_num , p_data in self.data_dict[processes].items() :

        self.data_dict['p_number'] = self.p_num
        print(  '\n','_'*10,'\n' , self.data_dict , '\n'    ,   '_'*10  , '8383\n'  )


proc_list = lines_of_input_file(test_path)
obj = RR(process_list=proc_list)



# make_out_file(test_dict)


























