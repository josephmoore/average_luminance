#!/usr/bin/python3
from PIL import Image, ImageStat
import sys
import os
from glob import glob
import multiprocessing
import argparse

# simple calculation of average pixel luminance of a given image or images
# requires Pillow, Pandas, and matplotlib
# can save data as csv and plot luminance of multiple images 
# currently most accurate when RGB images are 24bit and in the sRGB color space

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', help='source directory or image', required=True)
parser.add_argument('-t', '--ftype', help='image file type, e.g. jpg png')
parser.add_argument('-d', '--dest', help='destination .csv data file')
parser.add_argument('--plot', help='plot luminance values of images', action='store_true')
parser.add_argument('--stip-paths', help='strips paths of image files names in .csv', action='store_true')
args = parser.parse_args()

SRC = args.source
FTYPE = args.ftype
DST = args.dest
STRIPPATHS = args.strip_paths
# conversion matrix for rgb to gray
RGB2XYZ = (0.2125, 0.7154, 0.0721, 0,)


def get_image_paths(src_dir, ftype):
    img_paths = [f for f in glob(f"{src_dir}*.{ftype}")]
    return img_paths


def average_luma(imgname):
    img = Image.open(imgname)
    if img.mode == 'RGB':
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

        if args.plot is True:
            import matplotlib.pyplot as plt
            plot = True
        else:
            plot = False

        img_list = get_image_paths(SRC, FTYPE)
        fname_luma_list = get_all_lumas(img_list)

        if plot is True:
            fig = plt.figure()
            ax1 = fig.add_subplot(1, 1, 1)
            lumas = [x[1] for x in fname_luma_list]
            _ = ax1.hist(lumas, bins=255, color='k', alpha=0.5)
            plt.show()

        if DST is not None:
            from pandas import Series
            from natsort import natsorted

            sorted_by_fname = natsorted(fname_luma_list, key=lambda x: x[0])

            if STRIPPATHS is True:
                fl_series = Series({os.path.basename(f):l for f, l in sorted_by_fname})
            else:
                fl_series = Series({f:l for f, l in sorted_by_fname})

            fl_series.to_csv(DST, header=['average lumninance'], index_label='filename')

    elif os.path.isfile(SRC):
        print(average_luma(SRC))


if __name__ == "__main__":
    main()
