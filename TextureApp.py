# TODO: use matplotlib for demo??
import numpy as np
from PIL import Image

def synthesis(sample_image, output_width, output_height, block_size):
    output_image = Image.new('RGB', (output_width, output_height))
    overlap = int(block_size/6)

    for x in range(0, output_width-block_size, block_size-overlap):
        for y in range(0, output_height-block_size, block_size-overlap):
            # first block, chose random loc in sample, and create patch
            if x == 0 and y == 0:
                sample_x, sample_y = np.random.randint(0,sample_image.width), np.random.randint(0, sample_image.height)
                first_patch = sample_image.crop((sample_x, sample_y, sample_x+block_size, sample_y+block_size))
                first_patch.show()
                output_image.paste(first_patch)

            # elif x = 0: # first row
            #     # only overlap to left
            #     pass
            # elif y = 0: # first column
            #     # only overlap on tup
            #     pass
            else:
                pass


    return output_image