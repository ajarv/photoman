'''
Created on Dec 29, 2011

@author: AVashist
'''

import piexif
import os
import re
import sys
import time
import shutil
from os.path import join, getsize
from PIL import Image,ImageFilter
import argparse
import logging

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
            logging.error( '%r (%s) -> %r  ,%2.2f sec , FAIL' % \
                  (method.__name__, str(args), result, te - ts))
        return result
    return timed

@timeit_w_args_n_r
def get_image_creation_date_time(image_source_path):
    def dateFromExifInfo():
        try:
            exif_dict = piexif.load(image_source_path)
            ifd = "Exif"
            readable_dict = {piexif.TAGS[ifd][tag]["name"] : exif_dict[ifd][tag] for tag in exif_dict[ifd]}
            dateTimeTaken = readable_dict['DateTimeOriginal'].decode()
            dateTimeTaken = [ int(t) for t in dateTimeTaken.replace(":"," ").split(" ")]
            dateTimeTaken+=[0,0,0]
            dateTimeTaken = tuple(dateTimeTaken)
            return time.mktime(dateTimeTaken)
        except:
            logging.info("Failed to get Date from exif {0}".format( image_source_path))
            return None
        
    def dateFromFileCTime():
        mtime = os.path.getmtime(image_source_path)
        return mtime

    _t =  dateFromExifInfo() or dateFromFileCTime()
    return _t

@timeit_w_args_n_r
def resize_image(source_path, dest_path, size, ximage=None, quality=85, sharpen=True,_timeTaken=None):
    _dir = os.path.split(dest_path)[0]
    if not os.path.exists(_dir) : os.makedirs(_dir)


    if os.path.exists(dest_path):
        print ("Resized image exists -",dest_path)
        return

    timetaken = _timeTaken or get_image_creation_date_time(source_path)

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
    exif_bytes = piexif.dump(exif_dict)
    image.thumbnail(size, Image.ANTIALIAS )
    image = image.filter(ImageFilter.SHARPEN)
    image.save(_dest_path, "JPEG", quality=quality,exif_bytes=exif_bytes)
    # # copy EXIF data
    # sexif = pyexiv2.ImageMetadata(source_path)
    # sexif.read()
    # dexif = pyexiv2.ImageMetadata(_dest_path)
    # dexif.read()
    # sexif.copy(dexif)
    # # set EXIF image size info to resized size
    # dexif["Exif.Photo.PixelXDimension"] = image.size[0]
    # dexif["Exif.Photo.PixelYDimension"] = image.size[1]
    # dexif.write(preserve_timestamps=True)
    os.rename(_dest_path,dest_path)
    os.utime(dest_path,(timetaken,timetaken))



def orderFileList(file_paths):
    tree = {}
    for file_path in file_paths:
        _y,_m,_d  = time.localtime(os.path.getmtime(file_path))[0:3]
        yd = tree.get(_y,{}) ; tree[_y] = yd
        md = tree.get(_m,{}) ; tree[_m] = md
        dd = tree.get(_d,[]) ; tree[_d] = dd
        dd.append(file_path)

JPGPAT= re.compile(".*[.](jpg|nef)$",re.IGNORECASE)
MOVPAT= re.compile(".*[.](mp4|mov)$",re.IGNORECASE)

def process(source,destination):
    for root, dirs, files in os.walk(source):
        print ("Working on ",root)
        files =[file for file in files if JPGPAT.match(file) or MOVPAT.match(file)]
        #-- Date Groups
        file_paths = [join(root, name) for name in files]
        date_groups = {}
        for file_path in file_paths:
            _timetaken = get_image_creation_date_time(file_path)
            _tt = time.strftime('%Y-%m-%d',time.localtime(_timetaken))
            # _t = time.strftime('%y-%m-%d',time.localtime(os.path.getmtime(file_path)))
            _g = date_groups.get(_tt,[])
            _g.append([len(_g),_timetaken,_tt,file_path])
            date_groups[_tt] = _g
        jumbled_list = []
        for v in date_groups.values():
            jumbled_list.extend(v)
        jumbled_list.sort()
        jumbled_list = [ l[1:] for l in jumbled_list ]

        # for name in files:
        #     sfile = join(root, name)
        for (timetaken,timetakenstr,sfile) in jumbled_list:
            _dest = os.path.join(destination,'ORIGN',*timetakenstr.split('-'))
            file_name = os.path.split(sfile)[-1]
            dfile = os.path.join(_dest,file_name)
            ddir = os.path.dirname(dfile)
            if not os.path.exists(ddir):
                os.makedirs(ddir)
            if os.path.exists(dfile) :
                s1 ,s2 = os.path.getsize(dfile),os.path.getsize(sfile)
                if s1 >= s2:
                    print (sfile ," {1} -x- {0} >".format(s1,s2),dfile, ' ', timetakenstr)
                    os.remove(sfile)
                    print ("Removed ",sfile)
                    continue
                else:
                    print (sfile ," {1} -f- {0} >".format(s1,s2),dfile, ' ', timetakenstr)
                    dtemp = dfile+"_"
                    shutil.move(dfile,dtemp)
                    shutil.move(sfile,dfile)
                    os.remove(dtemp)
                    continue
            else:
                shutil.move(sfile,dfile)
                print (sfile ," ->",dfile, ' ', timetakenstr)
        try:
            os.removedirs(root)
            print ("Success   Remove ",root)
        except:
            print ("Failed to Remove ",root)
            pass

def make_tns(folder):
    origns = os.path.join(folder,'ORIGN')
    for root, dirs, files in sorted(os.walk(origns),reverse=True):
        print ("Working on ",root)
        files =[file for file in files if JPGPAT.match(file)]
        file_paths = [join(root, name) for name in files]
        for sfile in file_paths:
            dfile = sfile.replace("ORIGN",'S2000')
            resize_image(sfile,dfile,[2000,2000],quality=80)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Index Photos into a folder structure')
    parser.add_argument('--inputFolder', type=str, required=False,
                        default='sandbox',
                        help='Folder Path to Scan')
    parser.add_argument('--outputFolder', type=str, required=False,
                        default='vault',
                        help='Destination path for photos')
    return parser.parse_args()

			
			
if __name__ == "__main__":
    args = parse_args()
    process(args.inputFolder,args.outputFolder)
    make_tns(args.outputFolder)