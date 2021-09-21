
import math
import matplotlib.pyplot as plt
import openslide
from openslide import OpenSlideError
from openslide import deepzoom
import PIL
from PIL import Image
from IPython import display


SCALE_FACTOR = 32
interval = 32
index = (12, 47)




file="C:\\Users\es255022\\OneDrive - Teradata\\Desktop\\computational pathology\\WSI Images\\TCGA-A1-A0SP-01Z-00-DX1.20D689C6-EFA5-4694-BE76-24475A89ACC0.svs";

def open_slide(filename):

    try:
        slide = openslide.open_slide(filename)
    except OpenSlideError:
        slide = None
    except FileNotFoundError:
        slide = None
    return slide

def slide_to_scaled_pil_image(file):

    slide = open_slide(file)

    large_w, large_h = slide.dimensions
    new_w = math.floor(large_w / SCALE_FACTOR)
    new_h = math.floor(large_h / SCALE_FACTOR)
    level = slide.get_best_level_for_downsample(SCALE_FACTOR)
    print(slide.properties)
    whole_slide_image = slide.read_region((0, 0), level, slide.level_dimensions[level])
    whole_slide_image = whole_slide_image.convert("RGB")
    img = whole_slide_image.resize((new_w, new_h), PIL.Image.BILINEAR)

    plt.imshow(img)
    plt.show()

    return img


def slide_info(display_all_properties=False):

    slide = open_slide(file)
    print("Level count: %d" % slide.level_count)
    print("Level dimensions: " + str(slide.level_dimensions))
    print("Level downsamples: " + str(slide.level_downsamples))
    print("Level count: " + str(slide.level_downsamples))
    print("Dimensions: " + str(slide.dimensions))
    objective_power = int(slide.properties[openslide.PROPERTY_NAME_OBJECTIVE_POWER])
    print("Objective power: " + str(objective_power))
    image_size1 = slide.level_dimensions[0]
    image_size2 = slide.level_dimensions[1]
    image_size3 = slide.level_dimensions[2]
    print(image_size1, image_size2, image_size3)
    print("Slide Properties",slide.properties)
    region=slide.read_region((10002, 10002), 1, (512,512))
    for level in range(slide.level_count):
        scale = int(16 / slide.level_downsamples[level])  # Scale factor of the given level
        size = interval * scale  # Tile size depend on scale factor
        dimensions = (size, size)
        x, y = index[0] * interval * 16, index[
            1] * interval * 16  # Localisation from the level 0 => * max scale interval to get coordinate
        sample = slide.read_region((x, y), level, dimensions)

        # Display
        print('tile:', index, '- level:', level, '- scale:', scale, '- size:', size)
        display(sample)
    print("best level to downsample"+str(slide.get_best_level_for_downsample(1)))
    zoom = openslide.deepzoom(slide, tile_size=254, overlap=1, limit_bounds=False)

    slide_to_scaled_pil_image(zoom)
    plt.imshow(zoom)
    plt.show()


slide_info()


