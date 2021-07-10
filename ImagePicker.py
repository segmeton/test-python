import random
import os
import os.path
from datetime import datetime
import shutil

def get_image_list():
    image_list = []

    for (dirpath, dirnames, filenames) in os.walk('images'):
        for f in filenames:
            if f.endswith(".jpg") or f.endswith(".png"):
                data = [f,os.path.join(dirpath, f)]
                image_list.append(data)

    return image_list

def sampling(list, n = 1):
    chosen = random.sample(list, n)
    return chosen

def copy_sampled_image(list):
    output_dir = output_path_generator("sampled")

    if not os.path.isdir(output_dir) :
        os.mkdir(output_dir)

    for name, dir in list:
        # print(f)
        shutil.copy(dir, f"{output_dir}/{name}")

def output_path_generator(filename):
    now = datetime.now()
    timestamp = now.strftime("%b-%d-%Y_%H-%M-%S")
    unix_timestamp = now.timestamp()
    output = f"output/{filename}-{timestamp}-{unix_timestamp}"
    return output