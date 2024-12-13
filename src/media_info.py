import datetime
import json
import re
import shutil
import sys
import timeit
from exifread import logger, process_file, exif_log, __version__ 
from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
import click
import os
@click.group()
@click.version_option(
    version="EXIF.py Version %s on Python%s" % (__version__, sys.version_info[0]),
    prog_name="EXIF.py",
    help="Extract EXIF information from digital image files."
)
def cli():
    pass

@cli.command()
@click.option(
    '-q', '--quick', is_flag=True, default=True,
    help="Do not process MakerNotes (default)."
)
@click.option(
    '-t', '--tag', type=str,
    help="Stop processing when this tag is retrieved."
)
@click.option(
    '-s', '--strict', is_flag=True,
    help="Run in strict mode (stop on errors)."
)
@click.option(
    '-d', '--debug', is_flag=True,
    help="Run in debug mode (display extra info)."
)
@click.option(
    '-c', '--color', is_flag=True,
    help="Output in color (only works with debug on POSIX)."
)
@click.option('--input-folder', type=click.Path(exists=True, file_okay=False), required=True, help='Path to the input folder')
@click.option('--output-folder', type=click.Path(exists=True, file_okay=False), required=True, help='Path to the output folder')
def process(quick, tag, strict, debug, color,input_folder,output_folder):
    exif_log.setup_logger(debug, color)
    
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if not (file.endswith(".JPG") or file.endswith(".jpeg")\
                or file.endswith(".jpg") or file.endswith(".png") ): continue
            print("working on file",file )
            filename = os.path.join(root, file)        
            rval = file_info(filename, quick, tag, strict, debug, color)
            createdDate = rval['createdTime'].split(" ")[0].replace("-","/")
            newFolder = f"{output_folder}/{createdDate}"
            os.makedirs(newFolder, exist_ok=True)
            newFile = os.path.join(newFolder, file)
            if os.path.exists(newFile): 
                continue
            try:
                shutil.move(filename,newFile)
                print (f"Moved to {filename} -> {newFile}")        
            except:
                print (f"Failed to move {filename} -> {newFile}")
                continue    


def file_info_(filename,quick, tag, strict, debug, color):
    escaped_fn  = filename.encode(
        sys.getfilesystemencoding(), 'surrogateescape'
        ).decode()

    file_start = timeit.default_timer()
    try:
        img_file = open(escaped_fn, 'rb')
    except IOError:
        logger.error("'%s' is unreadable", escaped_fn)
        return None

    tag_start = timeit.default_timer()

    # get the tags
    data = process_file(
        img_file, stop_tag=tag, details=quick, strict=strict, debug=debug
    )

    tag_stop = timeit.default_timer()

    if not data:
        # logger.warning('No EXIF information found')
        return None

    if 'JPEGThumbnail' in data:
        logger.info('File has JPEG thumbnail')
        del data['JPEGThumbnail']
    if 'TIFFThumbnail' in data:
        logger.info('File has TIFF thumbnail')
        del data['TIFFThumbnail']

    tag_keys = list(data.keys())
    tag_keys.sort()
    rval = {}
    for i in tag_keys:
        try:
            t, k, v = i, FIELD_TYPES[data[i].field_type][2], data[i].printable
            rval[str(t)] = v
        except:
            logger.error("%s : %s", i, str(data[i]))

    file_stop = timeit.default_timer()

    logger.debug("Tags processed in %s seconds", tag_stop - tag_start)
    logger.debug("File processed in %s seconds", file_stop - file_start)
    return rval

pat = re.compile('.*(?P<date_time>\d{4}.\d{2}.\d{2} \d{2}.\d{2}.\d{2}).*')

def extract_date_time(date_time :   str):
    m = pat.match(date_time)
    if m:
        return m.group("date_time")
    return None

def file_info(filename,quick, tag, strict, debug, color):
    rval = dict(filename=filename)    
    try:
        infodict = file_info_(filename,quick, tag, strict, debug, color)
        infodict = None
        if infodict: rval.update(infodict)
    except Exception as e:
        rval["error"] = f"failed file_file_info: {e}"
  
    createdTime = None 
    if createdTime is None:
        createdTime = extract_date_time(rval.get("EXIF DateTimeOriginal",""))
    if createdTime is None:
        createdTime = extract_date_time(rval.get("EXIF DateTimeDigitized",""))
    if createdTime is None:
        createdTime = datetime.datetime.fromtimestamp(os.path.getctime(filename)).strftime("%Y-%m-%d %H:%M:%S")
                    
    rval["createdTime"] = createdTime   
    return rval


if __name__ == '__main__':
    cli()