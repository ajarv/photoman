'''
Created on Dec 29, 2011

@author: AVashist
'''

import piexif
# import pyexiv2
import os
import re
import sys
import time
import shutil
from os.path import join, getsize
from PIL import Image,ImageFilter
import argparse
import logging
import i_util
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.WARN)

def timeit_w_args_n_r(method):
    def timed(*args, **kw):
        ts = time.time()
        #         print 'Begin -- %r (%s) ' % \
        #               (method.__name__, str(args))
        try:
            result = method(*args, **kw)
            te = time.time()
            logging.info( '%r (%s) -> %r  ,%2.2f sec , OK' % \
                  (method.__name__, str(args), result, te - ts))
        except:
            result = None
            te = time.time()
            logging.exception( '%r (%s) -> %r  ,%2.2f sec , FAIL' % \
                  (method.__name__, str(args), result, te - ts))
        return result
    return timed

def reject_file(origin_path):
    rfile = origin_path.replace('ORIGN','REJECT')
    dir_name,f = os.path.split(rfile)
    os.makedirs(dir_name,exist_ok=True)
    shutil.move(origin_path,rfile)
    print (f"Moved to Rejects {origin_path} -> {rfile}")

@timeit_w_args_n_r
def resize_image(source_path, dest_path, size, ximage=None, quality=85, sharpen=True,_timeTaken=None):
    _dir = os.path.split(dest_path)[0]
    if not os.path.exists(_dir) : os.makedirs(_dir)

    if os.path.exists(dest_path):
        print ("Resized image exists -",dest_path)
        return

    timetaken = _timeTaken or i_util.get_image_creation_date_time(source_path)

    _dest_path = dest_path+".tmp"
    if os.path.exists(_dest_path):
        os.remove(_dest_path)
    # resize image
    image = ximage or Image.open(source_path)
    exif_dict = piexif.load(source_path)
    # process im and exif_dict...
    w, h = image.size
    exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
    exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
    if 'thumbnail' in exif_dict:
        del exif_dict['thumbnail']
    exif_bytes = piexif.dump(exif_dict)
    try:
        image.thumbnail(size, Image.ANTIALIAS )
    except:
        reject_file(source_path)
        return False
    image = image.filter(ImageFilter.SHARPEN)
    image.save(_dest_path, "JPEG", quality=quality,exif_bytes=exif_bytes)
    # # # copy EXIF data
    # sexif = pyexiv2.ImageMetadata(source_path)
    # sexif.read()
    # dexif = pyexiv2.ImageMetadata(_dest_path)
    # dexif.read()
    # sexif.copy(dexif)
    # # # set EXIF image size info to resized size
    # dexif["Exif.Photo.PixelXDimension"] = image.size[0]
    # dexif["Exif.Photo.PixelYDimension"] = image.size[1]
    # dexif.write(preserve_timestamps=True)
    os.rename(_dest_path,dest_path)
    os.utime(dest_path,(timetaken,timetaken))
    return True


def orderFileList(file_paths):
    tree = {}
    for file_path in file_paths:
        _y,_m,_d  = time.localtime(os.path.getmtime(file_path))[0:3]
        yd = tree.get(_y,{}) ; tree[_y] = yd
        md = tree.get(_m,{}) ; tree[_m] = md
        dd = tree.get(_d,[]) ; tree[_d] = dd
        dd.append(file_path)

JPGPAT= re.compile(".*[.](jpg|nef|arw)$",re.IGNORECASE)
MOVPAT= re.compile(".*[.](mp4|mov)$",re.IGNORECASE)

def filtered_list(files):
    rfiles = []
    for file in files:
        try:
            image = Image.open(file)
            # process im and exif_dict...
            w, h = image.size
            l = max(w, h)
            if l >= 1200:
                rfiles.append(file)
            pass
        except :
            print(f"Possibly bad image file {file} skipping")
            reject_file(file)
            continue
            pass
    return rfiles

def build_file_set(destination_folder):
    rval = set()
    try:
        for root, dirs, files in os.walk(destination_folder):
            rval = rval.union(set( [join(root, name) for name in files]))
    except:
        logging.exception("Failed to generate the destination folder listing")
    return rval

def make_tns(folder):
    origns = os.path.join(folder,'ORIGN')
    existing_file_set = build_file_set(folder)
    for f in sorted(list(existing_file_set)):
        print (f)
    for root, dirs, files in sorted(os.walk(origns),reverse=True):
        print ("Working on ",root)
        files =[file for file in files if JPGPAT.match(file)]
        file_paths = [join(root, name) for name in files]
        file_paths = filtered_list(file_paths)
        for sfile in file_paths:
            if ' ' in sfile:
                sfile1 = sfile.replace(' ','-')
                os.rename(sfile,sfile1)
                sfile = sfile1
            dfile2000 = sfile.replace("ORIGN",'S2000')
            ok = True
            if dfile2000 not in existing_file_set and ok:
                ok = resize_image(sfile, dfile2000, [2000,2000], quality=75)
            dfile0300 = sfile.replace("ORIGN",'S0300')
            if dfile0300 not in existing_file_set and ok:
                resize_image(sfile, dfile0300, [300, 300], quality=65)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Index Photos into a folder structure')
    parser.add_argument('--vault', type=str, required=False,
                        default='vault',
                        help='Destination path for photos')
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    make_tns(args.vault)
