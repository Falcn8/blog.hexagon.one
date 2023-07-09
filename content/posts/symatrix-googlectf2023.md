---
title: "Symatrix Writeup Google CTF 2023"
date: 2023-07-09T14:21:13+09:00
description: "I solved Symatrix, one of of the challenges on Google CTF 2023."
tags: [ctf]
---

I solved **Symatrix**, one of of the challenges on Google CTF 2023. This challenge
was categorized in misc and it was a steganography challenge worth 114 points. So 
I'm writing my first CTF writeup.

## The Challenge

> The CIA has been tracking a group of hackers who communicate using PNG files 
embedded with a custom steganography algorithm.  
An insider spy was able to obtain the encoder, but it is not the original code.  
You have been tasked with reversing the encoder file and creating a decoder as 
soon as possible in order to read the most recent PNG file they have sent.

## Attachments

`encoder.c` - Looks like it's using Cython, "a superset of Python that allows 
you to write Python-like code with optional static typing, which can be 
compiled into highly optimized C/C++ extensions for improved performance".  

`symatrix.png` - Notice how the image is symmetric.
![picture of symatrix.png](/symatrix/symatrix.png "symatrix.png")

## Converting Cython to Python

The Cython file has 6810 lines so it took me a little time to figure out, but I 
noticed that from line 2620, it had a part of Python code commented like this.
```c
  #if defined(__Pyx_Generator_USED) || defined(__Pyx_Coroutine_USED)
  if (__Pyx_patch_abc() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif

  /* "encoder.py":1
 * from PIL import Image             # <<<<<<<<<<<<<<
 * from random import randint
 * import binascii
 */
  __pyx_t_1 = PyList_New(1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 1, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_INCREF(__pyx_n_s_Image);
``` 
Then, I pieced all of them together to create one Python file which looks like this.
```python
from PIL import Image
from random import randint
import binascii

def hexstr_to_binstr(hexstr):
    n = int(hexstr, 16)
    bstr = ''
    while n > 0:
        bstr = str(n % 2) + bstr
        n = n >> 1
    if len(bstr) % 8 != 0:
        bstr = '0' + bstr
    return bstr


def pixel_bit(b):
    return tuple((0, 1, b))


def embed(t1, t2):
    return tuple((t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2]))


def full_pixel(pixel):
    return pixel[1] == 255 or pixel[2] == 255

print("Embedding file...")

bin_data = open("./flag.txt", 'rb').read()
data_to_hide = binascii.hexlify(bin_data).decode('utf-8')

base_image = Image.open("./original.png")

x_len, y_len = base_image.size
nx_len = x_len * 2

new_image = Image.new("RGB", (nx_len, y_len))

base_matrix = base_image.load()
new_matrix = new_image.load()

binary_string = hexstr_to_binstr(data_to_hide)
remaining_bits = len(binary_string)

nx_len = nx_len - 1
next_position = 0

for i in range(0, y_len):
    for j in range(0, x_len):

        pixel = new_matrix[j, i] = base_matrix[j, i]

        if remaining_bits > 0 and next_position <= 0 and not full_pixel(pixel):
            new_matrix[nx_len - j, i] = embed(pixel_bit(int(binary_string[0])),pixel)
            next_position = randint(1, 17)
            binary_string = binary_string[1:]
            remaining_bits -= 1
        else:
            new_matrix[nx_len - j, i] = pixel
            next_position -= 1


new_image.save("./symatrix.png")
new_image.close()
base_image.close()

print("Work done!")
exit(1)
```

## Analyzing the Python File

I asked ChatGPT.

"Explain this program in 4 sentences"  
The code hides binary data within an image by modifying the pixel values. It reads 
binary data from a file and converts it to a binary string. Then, it iterates through 
the pixels of the image, embedding the binary data by modifying specific pixels based 
on certain conditions. The resulting image contains the hidden binary data.

"What do you mean by certain conditions"  
By "certain conditions," I mean specific criteria or requirements that must be met 
in order to embed the binary data into the image. In the given code, the conditions 
are:

1. The position in the image: The code checks if it's the appropriate position to 
embed a bit. This is determined by the variable next_position, which ensures that 
the bits are embedded at regular intervals.

2. Available space in the pixel: The code checks if the pixel has space available 
to embed the bit. This is determined by the function full_pixel, which checks if the 
pixel is fully white (255 in the green and blue channels). If the pixel is full, it 
means that no more data can be embedded in that pixel.

These conditions ensure that the binary data is embedded in a controlled manner, 
preserving the image quality while hiding the data within the pixel values.

--- 

Anyways, this program copies the original image to make the new image symmetric, then 
it goes through the newly copied image and edits the pixel to add part of the flag 
data. When it's embedding the hidden data to a pixel, it marks the pixel using the 
function `pixel_bit`.
```python
new_matrix[nx_len - j, i] = embed(pixel_bit(int(binary_string[0])),pixel)
```
When I looked into the function `pixel_bit`, it looks like it returns a certain value 
with the part of the flag data.
```python
def pixel_bit(b):
    return tuple((0, 1, b))
```
So, I noticed that I can just look for pixels that looks like `(0, 1, b)` and add up 
`b` to get the full flag data.

## Making the Decoder

I created the decoder with similar program to the encoder. Here's the decoder that I 
made:
```python
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
```
By running the decoder, the flag was outputted in `decoded_file.txt` with the flag 
`CTF{W4ke_Up_Ne0+Th1s_I5_Th3_Fl4g!}`

## Conclusion

It took me couple hours to solve this challenge, but I found it really fun solving it. 
Though I'm a little sad because I couldn't get to other challenges because I didn't 
have much time, I'm glad I was able to solve **Symatrix**. The files I used to solve 
**Symatrix** can be found [here](/symatrix/index.html). Thanks for reading my first 
writeup!

