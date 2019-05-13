import argparse
import pathlib
from PIL import Image


def main():
    # Parse args
    parser = argparse.ArgumentParser(description='Quickly generate variable sized images in next-gen image formats.')
    parser.add_argument('paths', metavar='paths', type=str, nargs='+', help='a list of file paths to view')
    parser.add_argument('-E', '--extensions', type=str, nargs='*', help='specifies the extensions e.g. *.jpg, *.png')
    parser.add_argument('-R', '--recursive', action='store_true', help='sets app to crawl images recurively')
    args = parser.parse_args()

    # Parse and generate paths
    paths = [path for path in args.paths if pathlib.Path(path).exists()]
    print("PATHS:", paths)

    # Parse and generate extensions
    infile_ext = ['*.jpg', '*.png']
    if args.extensions:
        infile_ext = ["*{}".format(x) if x.startswith('.') else "*.{}".format(x) if not x.startswith('*.') else x for x in args.extensions]
    if args.recursive:
        infile_ext = ["**/" + x for x in infile_ext]
    print("INFILE EXT:", infile_ext)

    # Parse and generate extensions
    outfile_ext = ['.webp', '.jp2']
    print("OUTFILE EXT:", outfile_ext)

    # Parse and generate media widths
    media_widths = [1600, 1200, 800, 600, 400, 200, 100]
    print("MEDIA WIDTHS:", media_widths)

    # Generate search paths
    files = []
    for path in paths:
        filepath = pathlib.Path(path)
        for pattern in infile_ext:
            files.extend([x for x in filepath.glob(pattern)])

    # Generate conversion sequence
    convseq = []
    for infile in files:
        for ext in outfile_ext:
            for width in media_widths:
                filepath = pathlib.Path(infile)
                parent = filepath.parent
                stem = filepath.stem
                convseq.append(("{}".format(infile), "{}/{}-{}{}".format(parent, stem, width, ext), width))

    # Iterate over conversion sequence
    for infile, outfile, width in convseq:
        if infile != outfile:
            try:
                print("Converting {} to {}".format(infile, outfile))
                
                # Open file
                img = Image.open(infile)

                # Set new image size
                max_width = width
                max_height = img.width

                # Resize image
                img.thumbnail((max_width, max_height), Image.LANCZOS)

                # Export image file
                img.save(outfile)

            except IOError:
                print("Conversion failed:", infile, outfile)

if __name__ == "__main__":
    main()
