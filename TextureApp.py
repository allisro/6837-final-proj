# TODO: use matplotlib for demo??
import numpy as np
import random
from itertools import product
from PIL import Image

def precompute_blocks(sample_image, block_size):
    blocks = []
    for i,j in product(range(sample_image.width-block_size), range(sample_image.height-block_size)):
        block = sample_image.crop((i, j, i+block_size, j+block_size))
        blocks.append(block)
    return blocks

def synthesis(sample_image, output_width, output_height, block_size):
    output_image = Image.new('RGB', (output_width, output_height))
    overlap = int(block_size/6)
    blocks = precompute_blocks(sample_image, block_size)

    for x in range(0, output_width-block_size, block_size-overlap):
        for y in range(0, output_height-block_size, block_size-overlap):
            # first block, chose random loc in sample, and create patch
            if x == 0 and y == 0:
                #sample_x, sample_y = np.random.randint(0,sample_image.width), np.random.randint(0, sample_image.height)
                #first_patch = sample_image.crop((sample_x, sample_y, sample_x+block_size, sample_y+block_size))
                first_patch = random.choice(blocks)
                output_image.paste(first_patch)

            elif x == 0: # first column
                # only overlap on top
                prev_block = output_image.crop((0, y-block_size, block_size, y))
                patch = findBestPatch(sample_image, blocks, prev_block, output_width, output_height, block_size, False, True)
                output_image.paste(patch,(x,y-overlap))
            # elif y = 0: # first row
            #     # only overlap to left
            #     pass
            else:
                pass
    return output_image


def findBestPatch(sample_image, blocks, previous_block, output_width, output_height, block_size, horizontal, vertical):
    errors = []
    tolerance = 0.1
    overlap = int(block_size/6)
    
    for block in blocks:
        if horizontal:
            pass
        if vertical:
            prev_overlap = previous_block.crop((0, block_size-overlap, block_size, block_size)) # bottom overlap
            sample_overlap = block.crop((0,0, block_size, overlap)) # top overlap
            ssd = 0
            for x in range(overlap):
                for y in range(overlap):
                    ssd_r = ((sample_overlap.getpixel((x,y))[0] - prev_overlap.getpixel((x,y))[0])**2)**0.5
                    ssd_g = ((sample_overlap.getpixel((x,y))[1] - prev_overlap.getpixel((x,y))[1])**2)**0.5
                    ssd_b = ((sample_overlap.getpixel((x,y))[2] - prev_overlap.getpixel((x,y))[2])**2)**0.5
                    ssd += (ssd_r + ssd_b + ssd_g)/3
            errors.append(ssd)

    min_error = min(errors)
    candidates = list(filter(lambda x: x <= min_error+tolerance*min_error, errors))
    ind = errors.index(random.choice(candidates))

    return blocks[ind]



