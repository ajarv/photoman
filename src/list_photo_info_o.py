
import sys
import argparse
import logging
import timeit
from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
from exifread import process_file, exif_log, __version__
import os

logger = exif_log.get_logger()


def get_args():
    parser = argparse.ArgumentParser(
        prog='EXIF.py',
        description='Extract EXIF information from digital image files.'
    )
    parser.add_argument(
        'files', metavar='FILE', type=str, nargs='+',
        help='files to process',
    )
    parser.add_argument(
        '-v', '--version', action='version',
        version='EXIF.py Version %s on Python%s' % (__version__, sys.version_info[0]),
        help='Display version information and exit'
    )
    parser.add_argument(
        '-q', '--quick', action='store_false', dest='detailed',
        help='Do not process MakerNotes',
    )
    parser.add_argument(
        '-t', '--tag', type=str, dest='stop_tag',
        help='Stop processing when this tag is retrieved.',
    )
    parser.add_argument(
        '-s', '--strict', action='store_true', dest='strict',
        help='Run in strict mode (stop on errors).',
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', dest='debug',
        help='Run in debug mode (display extra info).',
    )
    parser.add_argument(
        '-c', '--color', action='store_true', dest='color',
        help='Output in color (only works with debug on POSIX).',
    )
    args = parser.parse_args()
    return args


def get_info(filename: str) -> dict:
    exif_log.setup_logger(args.debug, args.color)
    escaped_fn = escaped_fn = filename.encode(
        sys.getfilesystemencoding(), 'surrogateescape'
        ).decode()

    file_start = timeit.default_timer()
    try:
        img_file = open(escaped_fn, 'rb')
    except IOError:
        logger.error("'%s' is unreadable", escaped_fn)
        return None
    logger.info('Opening: %s', escaped_fn)

    tag_start = timeit.default_timer()

    # get the tags
    data = process_file(
        img_file, stop_tag=args.stop_tag, details=args.detailed, strict=args.strict, debug=args.debug
    )

    tag_stop = timeit.default_timer()

    if not data:
        logger.warning('No EXIF information found')
        print()
        return None

    if 'JPEGThumbnail' in data:
        logger.info('File has JPEG thumbnail')
        del data['JPEGThumbnail']
    if 'TIFFThumbnail' in data:
        logger.info('File has TIFF thumbnail')
        del data['TIFFThumbnail']

    tag_keys = list(data.keys())
    tag_keys.sort()
    rval = { }
    for i in tag_keys:
        try:
            t, k, v = i, FIELD_TYPES[data[i].field_type][2], data[i].printable
            logger.info(
                '%s (%s): %s', t,k,v)
            rval[k] = (t,k,v)
        except:
            logger.error("%s : %s", i, str(data[i]))

    file_stop = timeit.default_timer()

    logger.debug("Tags processed in %s seconds", tag_stop - tag_start)
    logger.debug("File processed in %s seconds", file_stop - file_start)
    print()
    return rval

def main(args) -> None:
    """Extract tags based on options (args)."""

    exif_log.setup_logger(args.debug, args.color)

    # output info for each file
    for filename in args.files:
        # avoid errors when printing to console
        escaped_fn = escaped_fn = filename.encode(
            sys.getfilesystemencoding(), 'surrogateescape'
        ).decode()

        file_start = timeit.default_timer()
        try:
            img_file = open(escaped_fn, 'rb')
        except IOError:
            logger.error("'%s' is unreadable", escaped_fn)
            continue
        logger.info('Opening: %s', escaped_fn)

        tag_start = timeit.default_timer()

        # get the tags
        data = process_file(
            img_file, stop_tag=args.stop_tag, details=args.detailed, strict=args.strict, debug=args.debug
        )

        tag_stop = timeit.default_timer()

        if not data:
            logger.warning('No EXIF information found')
            print()
            continue

        if 'JPEGThumbnail' in data:
            logger.info('File has JPEG thumbnail')
            del data['JPEGThumbnail']
        if 'TIFFThumbnail' in data:
            logger.info('File has TIFF thumbnail')
            del data['TIFFThumbnail']

        tag_keys = list(data.keys())
        tag_keys.sort()

        for i in tag_keys:
            try:
                logger.info('%s (%s): %s', i, FIELD_TYPES[data[i].field_type][2], data[i].printable)
            except:
                logger.error("%s : %s", i, str(data[i]))

        file_stop = timeit.default_timer()

        logger.debug("Tags processed in %s seconds", tag_stop - tag_start)
        logger.debug("File processed in %s seconds", file_stop - file_start)
        print()

def isImage(name):
    return name.split('.')[-1].lower() in ["jpg",'jpeg']

def do_files(files,args):
    for filename in files:
        # avoid errors when printing to console
        escaped_fn = escaped_fn = filename.encode(
            sys.getfilesystemencoding(), 'surrogateescape'
        ).decode()

        file_start = timeit.default_timer()
        try:
            img_file = open(escaped_fn, 'rb')
        except IOError:
            logger.error("'%s' is unreadable", escaped_fn)
            continue
        logger.info('Opening: %s', escaped_fn)

        tag_start = timeit.default_timer()

        # get the tags
        data = process_file(
            img_file, stop_tag=args.stop_tag, details=args.detailed, strict=args.strict, debug=args.debug
        )

        tag_stop = timeit.default_timer()

        if not data:
            logger.warning('No EXIF information found')
            print()
            continue

        if 'JPEGThumbnail' in data:
            logger.info('File has JPEG thumbnail')
            del data['JPEGThumbnail']
        if 'TIFFThumbnail' in data:
            logger.info('File has TIFF thumbnail')
            del data['TIFFThumbnail']

        tag_keys = list(data.keys())
        tag_keys.sort()

        for i in tag_keys:
            try:
                logger.info(
                    '%s (%s): %s', i, FIELD_TYPES[data[i].field_type][2], data[i].printable)
            except:
                logger.error("%s : %s", i, str(data[i]))

        file_stop = timeit.default_timer()

        logger.debug("Tags processed in %s seconds", tag_stop - tag_start)
        logger.debug("File processed in %s seconds", file_stop - file_start)
        print()

def main2(args) -> None:
    base_dir = args.base_dir
    for root, dirs, files in os.walk(base_dir, topdown=False):
        _files = [os.path.join(root, name) for name in files if isImage(name)]

        do_files(_files,args)


if __name__ == '__main__':
    args = get_args()
    # main(args)
    z = get_info(sys.argv[1])
    print(z)