import os
import argparse
from blender_utils import *


def main():
    """
    Render a mesh from an OFF file.
    """

    parser = argparse.ArgumentParser(description='Renders a mesh (OFF file).')
    parser.add_argument('--off', type=str, help='Path to OFF file.')
    parser.add_argument('--output', type=str, default='output.png', help='Path to output PNG image.')

    try:
        argv = sys.argv[sys.argv.index("--") + 1:]
    except ValueError:
        argv = ""
    args = parser.parse_args(argv)

    if not os.path.exists(args.off):
        log('OFF file not found.', LogLevel.ERROR)
        exit()

    camera_target = initialize()
    off_material = make_material('BRC_Material_Mesh', (0.66, 0.45, 0.23), 0.8, True)

    load_off(args.off, off_material, (-0.5, -0.5, -0.5), 0.03125, 'xzy')

    rotation = (5, 0, -55)
    distance = 0.5
    render(camera_target, args.output, rotation, distance)


if __name__ == '__main__':
    main()
