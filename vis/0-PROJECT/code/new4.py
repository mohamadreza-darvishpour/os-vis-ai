import os
import cv2
import numpy as np

def get_image_files_path_list(directory_path):
    """
    Get all image files (.jpg, .png, .jpeg) in the specified directory.

    Parameters:
        directory_path (str): The path to the directory.

    Returns:
        list: A list of image file paths in the directory.
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")

    image_extensions = {'.jpg', '.jpeg', '.png'}
    image_files = []

    # Iterate over files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        # Check if the file is a valid image based on its extension
        if os.path.isfile(file_path) and os.path.splitext(file_name.lower())[1] in image_extensions:
            image_files.append(f'{directory_path}/{file_name}')

    return image_files

def enhance_image(image):
    """
    Enhance the image by applying color filtering and edge enhancement.

    Parameters:
        image (numpy.ndarray): The image to be enhanced.

    Returns:
        numpy.ndarray: The enhanced image.
    """
    # Convert to LAB color space for better contrast enhancement
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    l, a, b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_lab_image = cv2.merge((cl, a, b))
    
    # Convert back to BGR
    enhanced_image = cv2.cvtColor(enhanced_lab_image, cv2.COLOR_LAB2BGR)
    
    # Apply Edge Enhancement (using Canny Edge detection)
    edges = cv2.Canny(enhanced_image, 100, 200)
    
    # Use edges to create an overlay image with enhanced edges
    enhanced_image = cv2.bitwise_and(enhanced_image, enhanced_image, mask=edges)
    
    return enhanced_image

def calculate_histogram(image, channel_index):
    """
    Calculate the normalized histogram of a specific channel of the image.

    Parameters:
        image (numpy.ndarray): The image in BGR format (OpenCV format).
        channel_index (int): The index of the channel to calculate the histogram for (0 = Blue, 1 = Green, 2 = Red).

    Returns:
        numpy.ndarray: The normalized histogram of the selected channel.
    """
    # Extract the selected channel
    channel_image = image[:, :, channel_index]
    
    # Compute histogram for the selected channel
    hist = cv2.calcHist([channel_image], [0], None, [256], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()  # Normalize and flatten the histogram
    
    return hist

def calculate_histogram_similarity(hist1, hist2):
    """
    Calculate similarity between two histograms using correlation.

    Parameters:
        hist1 (numpy.ndarray): The first image histogram.
        hist2 (numpy.ndarray): The second image histogram.

    Returns:
        float: The similarity score (higher is more similar).
    """
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity

def compare_images(test_image_path, dataset_image_paths, channel_weights=(1, 1, 1)):
    """
    Compare a test image with all images in a dataset based on histogram similarity for each channel,
    with customizable channel weights.

    Parameters:
        test_image_path (str): The path to the test image.
        dataset_image_paths (list): A list of image paths in the dataset.
        channel_weights (tuple): A tuple of three values indicating the weights for the Blue, Green, and Red channels.
        
    Returns:
        list: A list of tuples containing image paths and similarity scores.
    """
    # Read the test image
    test_image = cv2.imread(test_image_path)
    
    # Enhance the test image by applying color filter and edge enhancement
    enhanced_test_image = enhance_image(test_image)
    
    # Resize enhanced test image to a fixed size (optional but recommended for consistency)
    enhanced_test_image_resized = cv2.resize(enhanced_test_image, (400, 400))

    # Calculate the histograms for each channel (Blue, Green, Red) of the enhanced test image
    test_hist_b = calculate_histogram(enhanced_test_image_resized, 0)  # Blue channel
    test_hist_g = calculate_histogram(enhanced_test_image_resized, 1)  # Green channel
    test_hist_r = calculate_histogram(enhanced_test_image_resized, 2)  # Red channel

    similarities = []

    # Compare with all dataset images
    for dataset_image_path in dataset_image_paths:
        dataset_image = cv2.imread(dataset_image_path)
        
        # Enhance the dataset image by applying color filter and edge enhancement
        enhanced_dataset_image = enhance_image(dataset_image)
        
        # Resize enhanced dataset image to the same size as test image (for consistency)
        enhanced_dataset_image_resized = cv2.resize(enhanced_dataset_image, (400, 400))
        
        # Calculate the histograms for each channel (Blue, Green, Red) of the enhanced dataset image
        dataset_hist_b = calculate_histogram(enhanced_dataset_image_resized, 0)  # Blue channel
        dataset_hist_g = calculate_histogram(enhanced_dataset_image_resized, 1)  # Green channel
        dataset_hist_r = calculate_histogram(enhanced_dataset_image_resized, 2)  # Red channel

        # Calculate similarity for each channel
        similarity_b = calculate_histogram_similarity(test_hist_b, dataset_hist_b)
        similarity_g = calculate_histogram_similarity(test_hist_g, dataset_hist_g)
        similarity_r = calculate_histogram_similarity(test_hist_r, dataset_hist_r)

        # Apply the weights to each channel's similarity score
        weighted_similarity = (similarity_b * channel_weights[0] +
                               similarity_g * channel_weights[1] +
                               similarity_r * channel_weights[2]) / sum(channel_weights)

        similarities.append((dataset_image_path, weighted_similarity))

    # Sort by similarity (higher correlation means more similar)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities

def show_similar_images(similarities, num_images=3):
    """
    Show the most similar images from the dataset.

    Parameters:
        similarities (list): A list of tuples containing image paths and similarity scores.
        num_images (int): The number of similar images to show.
    """
    for i in range(min(num_images, len(similarities))):
        similar_image_path = similarities[i][0]
        similar_image = cv2.imread(similar_image_path)
        cv2.imshow(f"Similar Image {i + 1}", similar_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example Usage
picture_path = "dataset/banknote_test/im(5).jpg"
dataset_path = "dataset/banknote_dataset"

# Print the main picture (test image) name
print(f"Main Picture: {os.path.basename(picture_path)}")

# Get the list of dataset images
dataset_image_paths = get_image_files_path_list(dataset_path)

# Set the weights for Blue, Green, and Red channels (for example, we give more weight to the Blue channel)
channel_weights = (100, 1, 10.5)  # Blue: 0.5, Green: 1, Red: 1.5

# Compare the test image with the dataset
similarities = compare_images(picture_path, dataset_image_paths, channel_weights=channel_weights)

# Print the similarity scores in ascending order
print("Similarity Scores (Descending Order):")
for dataset_image_path, similarity in similarities:
    print(f"Image: {dataset_image_path}, Similarity Score: {similarity:.4f}")

# Show the most similar images
show_similar_images(similarities, num_images=3)
