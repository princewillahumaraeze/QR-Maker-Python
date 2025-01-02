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

    def add_finder_pattern(x, y):
        """ Add finder pattern at a specific position in the matrix """
        for i in range(-4, 5):
            for j in range(-4, 5):
                if (abs(i) == 4 or abs(j) == 4) or (abs(i) == 2 and abs(j) == 2):
                    qr_matrix[y + i][x + j] = 1

    # Add finder patterns (top-left, top-right, bottom-left)
    add_finder_pattern(4, 4)
    add_finder_pattern(size - 5, 4)
    add_finder_pattern(4, size - 5)

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
        x, y, direction = size - 1, size - 1, -1
        for bit in ''.join(format(ord(char), '08b') for char in data):
            while qr_matrix[y][x] != 0:
                x -= 1
                if x < 0:
                    x, y = size - 1, y + direction
                    if y < 0 or y >= size:
                        direction *= -1
                        y += direction

            qr_matrix[y][x] = int(bit)

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
    data = 'Hello, World!'
    qr_code = generate_qr(data)
    print("QR Code printed in the console:")
    print(qr_code)
    print("\nVisualizing QR Code...")
    visualize_qr_code(qr_code)


if __name__ == '__main__':
    main()
