#!/usr/bin/python3
from PIL import Image, ImageStat
import sys
import os
from glob import glob
import multiprocessing
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', help='source directory or image', required=True)
parser.add_argument('-t', '--ftype', help='image file type, e.g. jpg png')
parser.add_argument('-d', '--dest', help='destination directory')
parser.add_argument('--plot', help='plot luminance values of images', action='store_true')
args = parser.parse_args()

plot = False
if args.plot is True and os.path.isdir(args.source):
    import matplotlib.pyplot as plt
    plot = True

SRC = args.source
FTYPE = args.ftype
DST = args.dest

# conversion matrix for rgb to gray
RGB2XYZ = (0.2125, 0.7154, 0.0721, 0,)


def get_image_paths(src_dir, ftype):
    img_paths = [f for f in glob(f"{src_dir}*.{ftype}")]
    return img_paths


def average_luma(imgname):
    img = Image.open(imgname)
    if img.mode is 'RGB':
        img = img.convert('L', RGB2XYZ)
    return (imgname, ImageStat.Stat(img).mean[0])


def get_all_lumas(img_list):
    with multiprocessing.Pool(processes=4) as pool:
        fl = pool.map(average_luma, img_list)
        return fl


def main():
    if os.path.isdir(SRC):
        if FTYPE is None:
            print("specify a file type when sourcing from a directory")
            sys.exit()
        img_list = get_image_paths(SRC, FTYPE)
        fname_luma_list = get_all_lumas(img_list)
        if plot is True:
            lumas = [x[1] for x in fname_luma_list]
            _ = plt.hist(lumas, bins=255, color='k', alpha=0.5)
            plt.show()

    elif os.path.isfile(SRC):
        print(average_luma(src))


if __name__ == "__main__":
    main()
