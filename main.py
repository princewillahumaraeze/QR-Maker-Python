import matplotlib.pyplot as plt


def generate_qr(data: str, size: int = 21) -> list:
    """
    Generate a qr code from the given data

    :param data: Data to encode in the qr code
    :param size: The size of the qr code(must be odd)
    :return: 2d matrix representing the qr code
    """
    if size < 21 or size % 2 == 0:
        raise ValueError('Size must be greater than 21 and odd')

    qr_matrix = [[0 for _ in range(size)] for _ in range(size)]

    # data = [int(bit) for bit in bin(ord(char))[2:].zfill(8) for char in input]
    data_bits = [int(bit) for char in data for bit in bin(ord(char))[2:].zfill(8)]

    def add_finder_pattern(x, y):
        """ Add finder pattern at a specific position in the matrix """
        for i in range(7):
            for j in range(7):
                # Outer black square
                if i == 0 or i == 6 or j == 0 or j == 6:
                    qr_matrix[x + i][y + j] = 1
                    # Inner black square (3x3)
                elif 2 <= i <= 4 and 2 <= j <= 4:
                    qr_matrix[x + i][y + j] = 1
                    # White spaces
                else:
                    qr_matrix[x + i][y + j] = 0

    # Add finder patterns (top-left, top-right, bottom-left)
    add_finder_pattern(0, 0)
    add_finder_pattern(0, size-7)
    add_finder_pattern(size-7, 0)

    def add_timing_patterns():
        """ Add timing patterns to the qr code matrix """
        for i in range(8, size - 8):
            if i % 2 == 0:
                qr_matrix[6][i] = 1
                qr_matrix[i][6] = 1

    add_timing_patterns()

    def encode_data():
        """Encodes the data into the qr code matrix"""
        # Simplistic data encoding ie: alternate bits along a zigzag path
        data_index = 0  # Initialize the index to the start of the data

        for i in range(size):  # Loop through rows
            for j in range(size):  # Loop through columns
                if qr_matrix[i][j] == 0:  # Check if the cell is empty
                    qr_matrix[i][j] = data_bits[data_index % len(data)]  # Assign data bit
                    data_index += 1  # Move to the next bit

    encode_data()

    return qr_matrix


def print_qr_code(matrix):
    """Prints the qr code matrix"""
    for row in matrix:
        print(''.join('█' if cell == 1 else ' ' for cell in row))


def visualize_qr_code(matrix):
    """Visualize the qr code matrix"""
    plt.figure(figsize=(8, 8))
    plt.imshow(matrix, cmap='binary', interpolation='nearest')
    plt.axis('off')
    plt.show()


def main():
    """ Main function to run the program"""
    data = 'https://www.google.com/'
    qr_code = generate_qr(data)
    print("QR Code printed in the console:")
    print(qr_code)
    print("\nVisualizing QR Code...")
    visualize_qr_code(qr_code)


if __name__ == '__main__':
    main()
