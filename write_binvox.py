import numpy as np
import argparse
import binvox_rw

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Write an example BINVOX file.')
    parser.add_argument('output', type=str, help='BINVOX file.')

    args = parser.parse_args()

    volume = np.zeros((32, 32, 32))
    volume[10:22, 10:22, 10:22] = 1

    model = binvox_rw.Voxels(volume > 0.5, volume.shape, (0, 0, 0), 1)
    with open(args.output, 'w') as fp:
        model.write(fp)
        print('Wote %s.' % args.output)