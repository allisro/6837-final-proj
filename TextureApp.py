import numpy as np
import random
from itertools import product
from PIL import Image
from skimage import io, util
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import videofig

animation = []

def precompute_blocks(sample_image, block_size):
    h, w, _ = sample_image.shape
    blocks = []
    for i,j in product(range(h-block_size), range(w-block_size)):
        block = sample_image[i:i+block_size, j:j+block_size]
        blocks.append(block)
    return blocks

def synthesis(image_file, block_size, num_blocks, sequence=False):
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
                #patch = random.choice(blocks)
                patch = findBestPatch(sample_image, res, blocks, overlap, block_size, i, j)
                patch = findMinPath(patch, res, overlap, block_size, i, j)

            res[i:i+block_size, j:j+block_size] = patch
            if sequence:
                # io.imshow(res)
                # io.show()
                animation.append(Image.fromarray((res * 255).astype(np.uint8)))

    output_image = Image.fromarray((res * 255).astype(np.uint8))
    #redraw_fn.initialized = False

    #videofig.videofig(len(animation), redraw_fn, play_fps=60)
    return output_image


def findBestPatch(sample_image, res, blocks, overlap, block_size, i, j):
    errors = []
    tolerance = 0.1
    
    for block in blocks:
        error = 0
        if j > 0: # left
            left = block[:, :overlap] - res[i:i+block_size, j:j+overlap]
            error += np.sum(left**2)
        if i > 0: # up
            up = block[:overlap, :] - res[i:i+overlap, j:j+block_size]
            error += np.sum(up**2)
        if j > 0 and i > 0: # need to get rid of corner once since calc twice
            corner = block[:overlap, :overlap] - res[i:i+overlap, j:j+overlap]
            error -= np.sum(corner**2)
        errors.append((error)**0.5)

    min_error = min(errors)
    candidates = list(filter(lambda x: x <= min_error+tolerance*min_error, errors))
    ind = errors.index(random.choice(candidates))

    return blocks[ind]

def findMinPath(patch, res, overlap, block_size, i ,j):
    patch = patch.copy()
    minCut = np.zeros_like(patch, dtype=bool)
    dy, dx, _ = patch.shape
    if j > 0:
        left = patch[:, :overlap] - res[i:i+dy, j:j+overlap]
        leftL2 = np.sum(left**2, axis=2)
        for y, x in enumerate(minCutPath(leftL2)):
            minCut[y, :x] = True
    if i > 0:
        up = patch[:overlap, :] - res[i:i+overlap, j:j+dx]
        upL2 = np.sum((up**2)**0.5, axis=2)
        for x, y in enumerate(minCutPath(upL2.T)):
            minCut[:y, x] = True

    np.copyto(patch, res[i:i+dy, j:j+dx], where=minCut)

    return patch

def minCutPath(errors):
    # dynamic programming, unused
    errors = np.pad(errors, [(0, 0), (1, 1)], 
                    mode='constant', 
                    constant_values=np.inf)

    cumError = errors[0].copy()
    paths = np.zeros_like(errors, dtype=int)    

    for i in range(1, len(errors)):
        M = cumError
        L = np.roll(M, 1)
        R = np.roll(M, -1)

        # optimize with np.choose?
        cumError = np.min((L, M, R), axis=0) + errors[i]
        paths[i] = np.argmin((L, M, R), axis=0)
    
    paths -= 1
    
    minCutPath = [np.argmin(cumError)]
    for i in reversed(range(1, len(errors))):
        minCutPath.append(minCutPath[-1] + paths[i][minCutPath[-1]])
    
    return map(lambda x: x - 1, reversed(minCutPath))


def redraw_fn(f, axes):
    img = animation[f]
    if not redraw_fn.initialized:
        redraw_fn.im = axes.imshow(img, animated=True)
        redraw_fn.initialized = True
    else:
        redraw_fn.im.set_array(img)

