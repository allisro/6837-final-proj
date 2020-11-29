import sys
from PIL import Image

import TextureApp

'''
Main driver, takes in sample image file, output image file, and block size of patch
'''
def main():
    args = sys.argv[1:]
    if (args < 3):
        print("Not enough arguments \n SAMPLE_IMAGE OUTPUT_IMAGE BLOCK_SIZE needed")
        return -1

    texture = TextureApp.synthesis(Image.open(args[0]), Image.open(args[1]), args[2])

    return texture

main()