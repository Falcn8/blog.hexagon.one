from PIL import Image

def binstr_to_hexstr(binstr):
    n = int(binstr, 2)
    return hex(n)[2:]

def full_pixel(pixel):
    return pixel[1] == 255 or pixel[2] == 255

def decode():
    encoded_image = Image.open("./symatrix.png")

    nx_len, y_len = encoded_image.size
    x_len = nx_len // 2

    encoded_matrix = encoded_image.load()

    binary_string = ""

    for i in range(0, y_len):
        for j in range(0, x_len):
            l = encoded_matrix[j, i]
            r = encoded_matrix[nx_len - j - 1, i]
            if l[0] == r[0] and l[1]+1 == r[1]:
                binary_string += str(r[2])

    hex_string = binstr_to_hexstr(binary_string)
    print(hex_string)
    decoded_data = bytes.fromhex(hex_string)

    with open('./decoded_file.txt', 'wb') as f:
        f.write(decoded_data)

    encoded_image.close()

    print("Decoding complete!")

decode()
