import sys
import piexif
import time
import os
import logging
import re

IMGPAT = re.compile(".*[.](jpeg|jpg|nef|arw)$", re.IGNORECASE)
JPGPAT = re.compile(".*[.](jpg|jpeg)$", re.IGNORECASE)
MOVPAT = re.compile(".*[.](mp4|mov)$", re.IGNORECASE)
DATEPAT_01 = re.compile(".*?(20[0-2][0-9]).*?([0-1][0-9]).*?([0-3][0-9]).*",
                        re.IGNORECASE)
logger = logging.getLogger(__file__)

def get_image_creation_date(image_source_path):
    def dateFromExifInfo():
        try:
            m = IMGPAT.match(image_source_path)
            if m:
                exif_dict = piexif.load(image_source_path)
                ifd = "Exif"
                readable_dict = {
                    piexif.TAGS[ifd][tag]["name"]: exif_dict[ifd][tag]
                    for tag in exif_dict[ifd]
                }
                dateTimeTaken = readable_dict['DateTimeOriginal'].decode()
                stamp = dateTimeTaken[:10].replace(':', '-')
                logger.info(f"EXIF Timestamp for {image_source_path} {stamp}")
                return stamp
            return None
        except:
            logger.info(
                "Failed to get Date from exif {0}".format(image_source_path))
            return None

    def dateFromFileName():
        try:
            d, f = os.path.split(image_source_path)
            m = DATEPAT_01.match(f)
            if m:
                stamp = '-'.join([t for t in m.groups()])
                logger.info(
                    f"DATE from FILENAME for {image_source_path} {stamp}")
                return stamp
            return None
        except:
            logger.info("Failed to get Date from file name {0}".format(
                image_source_path))
            return None

    def dateFromFileCTime():
        mtime = os.path.getmtime(image_source_path)
        stamp = time.strftime('%Y-%m-%d', time.localtime(mtime))
        logger.info(
            f"DATE from file Timestamp for {image_source_path} {stamp}")
        return stamp

    time_stamp = dateFromExifInfo() or dateFromFileName() or dateFromFileCTime(
    )
    return time_stamp

def get_image_creation_date_time(image_source_path):
    def dateFromExifInfo():
        try:
            exif_dict = piexif.load(image_source_path)
            ifd = "Exif"
            readable_dict = {
                piexif.TAGS[ifd][tag]["name"]: exif_dict[ifd][tag] for tag in exif_dict[ifd]}
            dateTimeTaken = readable_dict['DateTimeOriginal'].decode()
            dateTimeTaken = [int(t)
                             for t in dateTimeTaken.replace(":", " ").split(" ")]
            dateTimeTaken += [0, 0, 0]
            dateTimeTaken = tuple(dateTimeTaken)
            return time.mktime(dateTimeTaken)
        except:
            logging.info(
                "Failed to get Date from exif {0}".format(image_source_path))
            return None

    def dateFromFileName():
        try:
            d, f = os.path.split(image_source_path)
            m = DATEPAT_01.match(f)
            if m:
                stamp = time.mktime(tuple([int(t) for t in m.groups()]+[0,0,0,0,0,0]))
                logger.info(
                    f"DATE from FILENAME for {image_source_path} {stamp}")
                return stamp
            return None
        except:
            logger.info("Failed to get Date from file name {0}".format(
                image_source_path))
            return None

    def dateFromFileCTime():
        mtime = os.path.getmtime(image_source_path)
        return mtime

    _t = dateFromExifInfo() or dateFromFileName() or dateFromFileCTime()
    return _t

if __name__ == '__main__':
    ts = get_image_creation_date(sys.argv[1])
    print(ts)
