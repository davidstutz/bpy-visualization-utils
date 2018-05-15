import os
import argparse
from mesh import Mesh


def main():
    """
    Convert OFF to OBJ.
    """

    parser = argparse.ArgumentParser(description='Convert OFF to OBJ.')
    parser.add_argument('input', type=str, help='OFF file.')
    parser.add_argument('output', type=str, help='OBJ file.')

    args = parser.parse_args()
    if not os.path.exists(args.input):
        print('Input file does not exist.')
        exit(1)

    mesh = Mesh.from_off(args.input)
    print('Read %s.' % args.input)

    mesh.to_obj(args.output)
    print('Wrote %s.' % args.output)


if __name__ == '__main__':
    main()
