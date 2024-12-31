
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
        return []
    
    



adjacency_mat_ex = [
    [0 ,1 ,1 ,0 ,1 ,0 ,1],
    [1 ,0 ,1 ,0 ,0 ,0 ,0],
    [1 ,1 ,0 ,0 ,1 ,0 ,1],
    [0 ,0 ,0 ,0 ,0 ,1 ,0],
    [1 ,0 ,1 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,1 ,0 ,0 ,0],
    [1 ,0 ,1 ,0 ,0 ,0 ,0],
]
color_num = [ -1 , -1 , -1 , -1] 

obj = color_points_ids(adjacency_mat_ex , 3) 
print(obj.ids_coloring())






