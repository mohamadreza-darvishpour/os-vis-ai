
import cv2
import numpy as np

def compare_histograms(picture_path, dataset_paths):
    """
    Compare the histogram similarity of a given picture with a dataset of pictures.

    Args:
        picture_path (str): Path to the input picture.
        dataset_paths (list): List of paths to the dataset pictures.

    Returns:
        tuple: (most_similar_image_path, similarity_scores)
               - most_similar_image_path: The path of the most similar image.
               - similarity_scores: A dictionary with dataset image paths as keys and similarity scores as values.
    """
    # Load the input image
    input_image = cv2.imread(picture_path)
    if input_image is None:
        raise ValueError(f"Cannot load image: {picture_path}")

    # Convert the input image to RGB
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    # Calculate the histogram for the input image (R, G, B channels)
    input_hist = []
    for channel in range(3):  # R, G, B channels
        hist = cv2.calcHist([input_image], [channel], None, [256], [0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        input_hist.append(hist)

    similarity_scores = {}

    # Iterate through the dataset images
    for dataset_path in dataset_paths:
        # Load the dataset image
        dataset_image = cv2.imread(dataset_path)
        if dataset_image is None:
            print(f"Warning: Cannot load image: {dataset_path}")
            continue

        # Convert the dataset image to RGB
        dataset_image = cv2.cvtColor(dataset_image, cv2.COLOR_BGR2RGB)

        # Calculate the histogram for the dataset image (R, G, B channels)
        dataset_hist = []
        for channel in range(3):  # R, G, B channels
            hist = cv2.calcHist([dataset_image], [channel], None, [256], [0, 256])
            cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
            dataset_hist.append(hist)

        # Compare the histograms using correlation
        score = 0
        for i in range(3):  # Compare R, G, B channels
            score += cv2.compareHist(input_hist[i], dataset_hist[i], cv2.HISTCMP_CORREL)
        score /= 3  # Average similarity score across channels

        # Store the similarity score
        similarity_scores[dataset_path] = score

    # Find the most similar image
    most_similar_image_path = max(similarity_scores, key=similarity_scores.get)

    # Print similarity scores
    for path, score in similarity_scores.items():
        print(f"Similarity with {path}: {score:.4f}")

    # Return the most similar image and similarity scores
    return most_similar_image_path, similarity_scores


# Example usage
if __name__ == "__main__":
    input_image_path = "test_picture.jpg"
    dataset_image_paths = ["money1.jpg", "money2.jpg", "money3.jpg"]

    most_similar, scores = compare_histograms(input_image_path, dataset_image_paths)
    print(f"\nMost similar image: {most_similar}")
