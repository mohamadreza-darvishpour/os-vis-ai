import numpy as np
import sys



def lines_of_input_file(file_path):
    '''get the input file path and return (numpy) matris'''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for index in range(len(lines)):
                lines[index]  = lines[index].strip().split()
            for time in range(60):
                try:lines.remove([]) 
                except: pass
        return np.array(lines , dtype=int)

    except FileNotFoundError:
        print(f"\nError: The file at {file_path} was not found.\n")
        return''
    except Exception as e:
        print(f"\nError reading file: {e}\n")
        return''


def make_out_file(result:str):
    try :
        file_name = 'output.txt'
        with open(f'{file_name}', 'w', encoding='utf-8') as file:
            file.write(result)
        print(f"result : {result}\nFile '{file_name}' created successfully.\n")

    except Exception as e : 
        print(f'\nerror making output file. \n')



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










def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python myfile.py <input.txt> (adjacency matrix)")
            sys.exit(1)

        input_file_path = sys.argv[1]
        input_adjacency = lines_of_input_file(input_file_path)
        print(input_adjacency,'\n')
        num_type_color = 4
        ids_obj = color_points_ids(adjacency_mat=input_adjacency , num_colors=num_type_color)
        ids_obj.ids_coloring() 
        out_put_text = ids_obj.color_result()
        make_out_file(out_put_text)
        
        print('\n\n\t<<done>>')
    
    except:
        print('\n\n\t\t\t<<error>>')

if __name__ == "__main__":
    main()







