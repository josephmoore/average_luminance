from PIL import Image, ImageStat
import PIL
import glob
import multiprocessing
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', help='source directory', required=True)
parser.add_argument('-t', '--ftype', help='image file type, e.g. jpg png, only required if dest=dir')
parser.add_argument('-d', '--dest', help='destination directory', required=True)
args = parser.parse_args()

src = args.source
ftype = args.ftype
dst = args.dest

SRC="/home/delta/Desktop/animals-2019-08-25/153.156.168.63_80/"

# conversion matrix for rgb to gray
RGB2XYZ = (0.2125, 0.7154, 0.0721, 0,)


def get_fnames(ftype):
    fnames = [f for f in glob.glob(f"{SRC}*.{ftype}")]
    return fnames


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
    fnames = get_fnames('jpg')
    fnames_lumas = get_all_lumas(fnames)
    return fnames_lumas


if __name__ == "__main__":
    main()
