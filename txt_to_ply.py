import os
import argparse
from point_cloud import PointCloud


def main():
    """
    Convert TXT to PLY.
    """

    parser = argparse.ArgumentParser(description='Convert TXT to PLY.')
    parser.add_argument('input', type=str, help='TXT file.')
    parser.add_argument('output', type=str, help='PLY file.')

    args = parser.parse_args()
    if not os.path.exists(args.input):
        print('Input file does not exist.')
        exit(1)

    point_cloud = PointCloud.from_txt(args.input)
    print('Read %s.' % args.input)

    point_cloud.to_ply(args.output)
    print('Wrote %s.' % args.output)


if __name__ == '__main__':
    main()
