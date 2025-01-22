test_path = 'dataset/banknote_test/im(1).jpg'    
dataset_folder = 'dataset/banknote_dataset'
from money import   get_image_files_path_list 
path_list  = get_image_files_path_list(dataset_folder)
#____________________________________________

from test import compare_histograms as com_hist 


#____________________________________________

print(com_hist(test_path , path_list) )
