import os
import argparse
from blender_utils import *


def main():
    """
    Render a point cloud from a TXT file.
    """

    parser = argparse.ArgumentParser(description='Renders a mesh (OFF file) and a point cloud (TXT file) together.')
    parser.add_argument('--txt', type=str, help='Path to TXT file.')
    parser.add_argument('--output', type=str, default='output.png', help='Path to output PNG image.')

    try:
        argv = sys.argv[sys.argv.index("--") + 1:]
    except ValueError:
        argv = ""
    args = parser.parse_args(argv)

    if not os.path.exists(args.txt):
        log('TXT file not found.', LogLevel.ERROR)
        exit()

    camera_target = initialize()
    txt_material = make_material('BRC_Material_Point_Cloud', (0.65, 0.23, 0.25), 1, True)
    load_txt(args.txt, 0.0075, txt_material, (-0.5, -0.5, -0.5), 0.03125, 'xzy')

    rotation = (5, 0, -55)
    distance = 0.5
    render(camera_target, args.output, rotation, distance)


if __name__ == '__main__':
    main()
