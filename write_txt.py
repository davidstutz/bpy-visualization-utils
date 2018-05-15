import numpy as np
import argparse
from point_cloud import PointCloud


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Write an example point cloud as TXT.')
    parser.add_argument('output', type=str, help='TXT file for example point cloud.')

    args = parser.parse_args()
    point_cloud = PointCloud(np.random.random((100, 3)))
    point_cloud.to_txt(args.output)
    print('Wrote %s.' % args.output)
