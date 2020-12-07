import sys
from PIL import Image
import argparse
import os
import TextureApp

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image_path", required=True, type=str, help="path of image you want to quilt")
parser.add_argument("-b", "--block_size", type=int, default=50, help="block size in pixels")
parser.add_argument("-n", "--num_block", type=int, default=6, help="number of blocks you want")
parser.add_argument("-o","--output_file", required=True, type=str, help="Need output file path")
#parser.add_argument("-w","--output_width",required=True,type=int,help="Desired width of image")
#parser.add_argument("-h","--output_height",required=True,type=int,help="Desired height of image")
args = parser.parse_args()

'''
Main driver, takes in sample image file, output image file, and block size of patch
'''
if __name__ == "__main__":
    image_file = args.image_path
    block_size = args.block_size
    num_block = args.num_block
    output_texture = args.output_file
    #output_texture = args[1]
    #output_width = int(args[2])
    #output_height = int(args[3])
    

    if (block_size <= 0):
        sys.exit("Invalid block size")

    texture = TextureApp.synthesis(image_file, block_size, num_block) # texture an image
    texture.save(output_texture)
    

