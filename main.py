import sys
from PIL import Image

import TextureApp

'''
Main driver, takes in sample image file, output image file, and block size of patch
'''
if __name__ == "__main__":
    args = sys.argv[1:]
    if (len(args) < 5):
        sys.exit("Not enough arguments \n SAMPLE_IMAGE OUTPUT_TEXTURE WIDTH HEIGHT BLOCK_SIZE needed")

    sample_image = Image.open(args[0])
    output_texture = args[1]
    output_width = int(args[2])
    output_height = int(args[3])
    block_size = int(args[4])

    if (block_size <= 0):
        sys.exit("Invalid block size")

    texture = TextureApp.synthesis(sample_image, output_width, output_height, block_size) # texture an image
    texture.save(output_texture)
    

