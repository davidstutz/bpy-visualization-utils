import os
import argparse
from blender_utils import *


def main():
    """
    Main function for rendering a specific binvox file.
    """

    parser = argparse.ArgumentParser(description='Renders an occupancy grid (BINVOX file).')
    parser.add_argument('--binvox', type=str, help='Path to OFF file.')
    parser.add_argument('--output', type=str, default='output.png', help='Path to output PNG image.')

    try:
        argv = sys.argv[sys.argv.index("--") + 1:]
    except ValueError:
        argv = ""
    args = parser.parse_args(argv)

    if not os.path.exists(args.binvox):
        log('BINVOX file not found.', LogLevel.ERROR)
        exit()

    camera_target = initialize()
    binvox_material = make_material('BRC_Material_Occupancy', (0.66, 0.45, 0.23), 0.8, True)

    load_binvox(args.binvox, 0.0125, binvox_material, (0, 0, 0), (1, 1, 1), 'zxy')

    rotation = (5, 0, -55)
    distance = 0.5
    render(camera_target, args.output, rotation, distance)


if __name__ == '__main__':
    main()
