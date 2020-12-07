import numpy as np
import random
from itertools import product
from PIL import Image
from skimage import io, util

def precompute_blocks(sample_image, block_size):
    h, w, _ = sample_image.shape
    blocks = []
    for i,j in product(range(h-block_size), range(w-block_size)):
        block = sample_image[i:i+block_size, j:j+block_size]
        blocks.append(block)
    return blocks

def synthesis(image_file, block_size, num_blocks):
    sample_image = Image.open(image_file)
    sample_image = util.img_as_float(sample_image)
    overlap = int(block_size/6)
    output_width = num_blocks*block_size  - (num_blocks - 1) * overlap # second part is overlap area we need to subtract
    output_height = num_blocks*block_size - (num_blocks - 1) * overlap
    blocks = precompute_blocks(sample_image, block_size)

    res = np.zeros((output_height, output_width, sample_image.shape[2]))

    for y in range(num_blocks): # rows
        for x in range(num_blocks): # cols
            i = y * (block_size - overlap)
            j = x * (block_size - overlap)

            # first block, chose random loc in sample, and create patch
            if x == 0 and y == 0:
                patch = random.choice(blocks)

            else:
                patch = findBestPatch(sample_image, res, blocks, overlap, block_size, i, j)

            res[i:i+block_size, j:j+block_size] = patch

    output_image = Image.fromarray((res * 255).astype(np.uint8))
    return output_image


def findBestPatch(sample_image, res, blocks, overlap, block_size, i, j):
    #h, w, _ = sample_image.shape
    #errors = np.zeros((h - block_size, w - block_size))
    errors = []
    tolerance = 0.1
    
    for block in blocks:
        error = 0
        if j > 0: # left
            left = block[:, :overlap] - res[i:i+block_size, j:j+overlap]
            error += np.sum(left**2)
        if i > 0: # right
            up = block[:overlap, :] - res[i:i+overlap, j:j+block_size]
            error += np.sum(up**2)
        if j > 0 and i > 0: # need to get rid of corner once since calc twice
            corner = block[:overlap, :overlap] - res[i:i+overlap, j:j+overlap]
            error -= np.sum(corner**2)
        #errors[i, j] = error
        errors.append(error)

    min_error = min(errors)
    candidates = list(filter(lambda x: x <= min_error+tolerance*min_error, errors))
    ind = errors.index(random.choice(candidates))

    return blocks[ind]



