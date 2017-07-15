from PIL import Image

image = Image.open("littleschoolbus.bmp")
width, height = image.size
pixels = image.load()

flag = ""

for x in range(width):
    pixel = pixels[x, height-1]
    for x in range(3)[::-1]: # Read BGR instead of RGB
        flag += bin(pixel[x])[-1]

print "".join(chr(int(flag[i:i+8], 2)) for i in xrange(0, len(flag), 8))

"""
After finding the original image, we can compare the difference between the two using imagemagick's compare command
$ compare littleschoolbus.bmp school\ bus.bmp -compose src diff.bmp

The only differences appear in the last row, so we know we need to perform LSB steganography on
the last row. By taking the last bit of each color (ordered BGR), we can construct another
binary string which will decode into the flag.

$ python solution.py
flag{remember_kids_protect_your_headers_afb3}ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ
"""
