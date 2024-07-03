import argparse

from Pylette import extract_colors


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--filename", help="path to image file", type=str, default=None)
    group.add_argument("--image-url", help="url to the image file", type=str, default=None)

    parser.add_argument(
        "--mode",
        help="extraction_mode (KMeans/MedianCut",
        type=str,
        default="KM",
        choices=["KM", "MC"],
    )
    parser.add_argument("--n", help="the number of colors to extract", type=int, default=5)
    parser.add_argument(
        "--sort_by",
        help="sort by luminance or frequency",
        default="luminance",
        type=str,
        choices=["luminance", "frequency"],
    )
    parser.add_argument(
        "--stdout",
        help="whether to display the extracted color values in the stdout",
        type=bool,
        default=True,
    )
    parser.add_argument(
        "--colorspace",
        help="color space to represent colors in",
        default="RGB",
        type=str,
        choices=["rgb", "hsv", "hls"],
    )
    parser.add_argument("--out_filename", help="where to save the csv file", default=None, type=str)
    parser.add_argument(
        "--display-colors",
        help="Open a window displaying the extracted palette",
        default=False,
        type=bool,
    )
    args = parser.parse_args()

    if args.filename is None and args.image_url is None:
        raise ValueError("Please provide either a filename or an image-url.")

    if args.filename is not None and args.image_url is not None:
        raise ValueError("Please provide either a filename or an image-url, not both.")

    if args.filename is not None and args.image_url is None:
        image = args.filename
    else:
        image = args.image_url

    palette = extract_colors(image=image, palette_size=args.n, sort_mode=args.sort_by)
    palette.to_csv(filename=args.out_filename, frequency=True, stdout=args.stdout)
    if args.display_colors:
        palette.display()


if __name__ == "__main__":
    main()
