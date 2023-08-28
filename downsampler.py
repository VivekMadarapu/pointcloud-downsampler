import numpy as np
import pandas as pd


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def as_array(self):
        return [self.x, self.y, self.z]


class Box:
    def __init__(self, c: Point, l: float, w: float, h: float):
        self.center = c
        self.length = l
        self.width = w
        self.height = h

    def contains(self, p: Point):
        return (p.x <= self.center.x + self.length) and (p.x >= self.center.x - self.length) and (
                p.y <= self.center.y + self.width) and (p.y >= self.center.y - self.width) and (
                p.z <= self.center.z + self.height) and (p.z >= self.center.z - self.height)


class Octree:
    def __init__(self, box: Box):
        self.box = box
        self.divided = False
        self.cum_points: [Point] = []
        self.subtrees: [Octree] = [None, None, None, None, None, None, None, None]

    def subdivide(self):
        l = self.box.length / 2
        w = self.box.width / 2
        h = self.box.height / 2
        self.subtrees = [
            Octree(Box(Point(self.box.center.x + l, self.box.center.y + w, self.box.center.z + h), l, w, h)),
            Octree(Box(Point(self.box.center.x + l, self.box.center.y + w, self.box.center.z - h), l, w, h)),
            Octree(Box(Point(self.box.center.x + l, self.box.center.y - w, self.box.center.z + h), l, w, h)),
            Octree(Box(Point(self.box.center.x + l, self.box.center.y - w, self.box.center.z - h), l, w, h)),
            Octree(Box(Point(self.box.center.x - l, self.box.center.y + w, self.box.center.z + h), l, w, h)),
            Octree(Box(Point(self.box.center.x - l, self.box.center.y + w, self.box.center.z - h), l, w, h)),
            Octree(Box(Point(self.box.center.x - l, self.box.center.y - w, self.box.center.z + h), l, w, h)),
            Octree(Box(Point(self.box.center.x - l, self.box.center.y - w, self.box.center.z - h), l, w, h))]

        self.divided = True

    def add_point(self, point):
        if not self.box.contains(point):
            return False

        self.cum_points.append(point)
        if not self.divided:
            self.subdivide()
            return True
        else:
            for i in range(8):
                inserted = self.subtrees[i].add_point(point)
                if inserted:
                    return True

        return False


def downsample(node, depth):
    if node is None:
        return
    if depth == res_depth and len(node.cum_points) > 0:
        p_arr = np.array([p.as_array() for p in node.cum_points])
        av_arr = np.average(p_arr, axis=0)
        downsampled_points.append(Point(av_arr[0], av_arr[1], av_arr[2]))
        return
    else:
        for c in range(8):
            downsample(node.subtrees[c], depth + 1)


if __name__ == '__main__':
    df = pd.read_csv('input.csv')

    octree = Octree(Box(Point(0.0, 0.0, 0.0), 10.0, 10.0, 10.0))

    print("Loading points...")
    for index, row in df.iterrows():
        octree.add_point(Point(row['x'], row['y'], row['z']))
    print("Points Loaded.")

    downsampled_points: [Point] = []
    res_depth = 8

    print("Downsampling...")
    downsample(octree, 0)
    print("Total points after downsample: " + str(len(downsampled_points)))

    with open('output.csv', 'w') as file:
        file.write("x,y,z\n")
        for i in range(len(downsampled_points)):
            file.write(
                str(downsampled_points[i].x) + "," + str(downsampled_points[i].y) + "," + str(
                    downsampled_points[i].z) + "\n")
