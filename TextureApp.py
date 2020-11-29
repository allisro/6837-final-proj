# TODO: use matplotlib for demo??

from PIL import Image

def synthesis(sample_image, output_image, block_size):
    overlap = block_size/6
    for x in range(output_image.width-block_size, block_size-overlap):
        for y in range(output_image.height-block_size, block_size-overlap):
            if x = 0 and y = 0: # first block
                # chose random loc in sample, and create patch?
            elif x = 0: # first row
                # only overlap to left
            elif y = 0: # first column
                # only overlap on tup
            else: