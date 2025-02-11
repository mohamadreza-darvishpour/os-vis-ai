import cv2
import numpy as np

def remove_salt_pepper_noise(image_path):
    """
    remove salt and pepper noise from an image using median filtering
    returns noise reduced image
    """
    img = cv2.imread(image_path)
    median_filtered_img = cv2.medianBlur(img, 5)  # Adjust kernel size as needed
    return median_filtered_img

def enhance_edges(image):
    """   returns image with enhanced edges"""
    #The surrounding elements (-1) subtract the intensity of neighboring pixels.
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])   
    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image

# Example usage:
i1 = "pr1/images/p1.png" 
i2 = "pr1/images/p2.jpg" 
i3 = "pr1/images/p3.jpg" 


def show_process(first_image):
    image_path = first_image
    first_pic = cv2.imread(image_path)
    print('\n\n\ndone\n\n\n')

    # Remove salt and pepper noise
    noise_reduced_image = remove_salt_pepper_noise(image_path)

    # Enhance edges in the noise-reduced image
    edge_enhanced_image = enhance_edges(noise_reduced_image)

    # Display the results
    cv2.imshow("Noise Reduced Image", noise_reduced_image)
    cv2.imshow("original pic ", first_pic)
    cv2.imshow("Edge Enhanced Image", edge_enhanced_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


show_process(i1)
show_process(i2)
show_process(i3)    #not gray scale


