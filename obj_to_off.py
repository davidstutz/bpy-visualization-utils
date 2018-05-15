import os
import argparse
from mesh import Mesh


def main():
    """
    Convert OBJ to OFF.
    """

    parser = argparse.ArgumentParser(description='Convert OBJ to OFF.')
    parser.add_argument('input', type=str, help='OBJ file.')
    parser.add_argument('output', type=str, help='OFF file.')

    args = parser.parse_args()
    if not os.path.exists(args.input):
        print('Input file does not exist.')
        exit(1)

    mesh = Mesh.from_obj(args.input)
    print('Read %s.' % args.input)

    mesh.to_off(args.output)
    print('Wrote %s.' % args.output)


if __name__ == '__main__':
    main()
