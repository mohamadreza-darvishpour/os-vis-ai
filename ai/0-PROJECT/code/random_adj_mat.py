import os
import random


def create_or_find_file_with_random_matrix(file_path):
    """
    Create or find a file and write a random upper triangular adjacency matrix.

    :param file_path: Path to the file where the matrix should be stored.
    """
    # Check if the file already exists
    # if os.path.exists(file_path):
    #     print(f"The file '{file_path}' already exists.")
    #     return

    # Generate a random size between 8 and 15
    size = random.randint(5,8)

    # Create an empty adjacency matrix
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    # Fill the upper triangular part randomly
    for i in range(size):
        for j in range(i + 1, size):
            value = random.randint(0, 1)  # Randomly choose 0 or 1
            matrix[i][j] = value
            matrix[j][i] = value  # Make it symmetric

    # Save the matrix to the file
    with open(file_path, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')
            
    file.close()
    print(f"The file '{file_path}' has been created and the matrix has been saved.")

