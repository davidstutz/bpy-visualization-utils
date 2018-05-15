import os
import numpy as np


class PointCloud:
    """
    Encapsulates a set of points stored as N x 3 matrix.
    """

    def __init__(self, points=None):
        """
        Constructor.

        :param points: points as list or np.array
        """

        if points is None:
            self.points = np.zeros((0, 3))
        else:
            self.points = np.array(points)

    @staticmethod
    def from_txt(filepath):
        """
        Load from TXT file.

        :param filepath: path to TXT file.
        :return: point cloud
        """

        assert os.path.exists(filepath)

        with open(filepath, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip() != '']

            num_points = int(lines[0])
            points = np.zeros((num_points, 3))
            assert num_points == len(lines) - 1

            for i in range(0, num_points):
                line = lines[i + 1]

                parts = line.split(' ')
                assert len(parts) == 3, "invalid line: %s" % line

                for j in range(3):
                    points[i, j] = float(parts[j])

        return PointCloud(points)

    def to_txt(self, filepath):
        """
        Write TXT.

        :param filepath: path to output file
        """
        with open(filepath, 'w') as f:
            f.write(str(self.points.shape[0]) + '\n')

            for n in range(self.points.shape[0]):
                f.write(str(self.points[n, 0]) + ' '  + str(self.points[n, 1]) + ' ' + str(self.points[n, 2]) + '\n')

    def to_ply(self, filepath):
        """
        To PLY file.

        :param filepath: path to output file
        """

        with open(filepath, 'w') as f:
            f.write('ply\n')
            f.write('format ascii 1.0\n')
            #f.write('format binary_little_endian 1.0\n')
            #f.write('format binary_big_endian 1.0\n')
            f.write('element vertex ' + str(self.points.shape[0]) + '\n')
            f.write('property float x\n')
            f.write('property float y\n')
            f.write('property float z\n')
            f.write('property uchar red\n')
            f.write('property uchar green\n')
            f.write('property uchar blue\n')
            f.write('end_header\n')

            for n in range(self.points.shape[0]):
                f.write(str(self.points[n, 0]) + ' '  + str(self.points[n, 1]) + ' ' + str(self.points[n, 2]))
                f.write(' 0 0 0\n')