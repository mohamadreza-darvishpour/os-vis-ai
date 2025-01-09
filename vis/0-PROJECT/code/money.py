

import os

def get_image_files(directory_path):
    """
    Get all image files (.jpg, .png, .jpeg) in the specified directory.

    Parameters:
        directory_path (str): The path to the directory.

    Returns:
        list: A list of image file names in the directory.
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
            image_files.append(file_name)

    return image_files

# Example usage:
if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    try:
        images = get_image_files(directory)
        print("Image files found:", images)
    except FileNotFoundError as e:
        print(e)





