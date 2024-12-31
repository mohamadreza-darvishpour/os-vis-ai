'''
input file structure 

1 0 0 1 0 1 1 1 1 0
...
1 ...   ....    ..1


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
                lines[index]  = np.array(lines[index].strip().split() , dtype=int)
        return np.array(lines)

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



import sys 
import numpy as np


class color_points_ids: 
    def __init__(self , adjacency_mat:np.ndarray , num_colors:int ):
        self.adjacency_mat = adjacency_mat 
        self.num_colors = num_colors 
        self.num_nodes =len(adjacency_mat)
        self.colors = [-1] * self.num_nodes 
        
    def is_valid_color(self , node:int , color: int) -> bool : 
        '''check if assigning color to node is valid'''
        for neighbor_ind in range(self.num_nodes): 
            if( self.adjacency_mat[node][neighbor_ind] ==1 and self.colors[neighbor_ind] == color):
                return False 
        return True 


    def dfs(self , node:int , depth:int) -> bool:
        '''first-depth-limited dfs for graph coloring '''
        if node == self.num_nodes:
            return True
        if depth == 0 :
            return False 
        
        for color in range(self.num_colors):
            if self.is_valid_color(node , color):
                self.colors[node] = color
                if self.dfs(node+1 , depth-1):
                    return True  
                self.colors[node] = -1  #backtrack when not ending.
        return False
    
    
        

    def ids_coloring(self) -> np.ndarray:
        '''perform IDS for graph coloring.'''
        for depth in range(1 , self.num_nodes+1):
            if self.dfs(0 , depth):
                return self.colors 
        return False
    
    

    def color_result(self) : 
        color_list  = ['red' , 'green' , 'blue' , 
                       'orange', 'white' , 'aqua' , 
                       'yellow' , 'purple' , 'black',]
        result_message ='' 
        if self.ids_coloring() ==False : 
            return 'error in \n\t\t1.adjacency matris\n\tor\n\t\t2.number of colors to use.\n'
        for ind in range(  len(self.colors)):
            #note to color_list[self.colors[ind]] it means get the color index number from colors in self 
            result_message += f'{ind}={color_list[self.colors[ind]]},'
        return result_message 






adjacency_mat_ex = [
    [0 ,1 ,1 ,0 ,1 ,0 ,1],
    [1 ,0 ,1 ,0 ,0 ,0 ,0],
    [1 ,1 ,0 ,0 ,1 ,0 ,1],
    [0 ,0 ,0 ,0 ,0 ,1 ,0],
    [1 ,0 ,1 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,1 ,0 ,0 ,0],
    [1 ,0 ,1 ,0 ,0 ,0 ,0],
]


obj  = color_points_ids(adjacency_mat_ex , 3)
obj.ids_coloring()
result = obj.color_result() 
print(result)







# print(lines_of_input_file(test_path))
# make_out_file(test_dict)
















