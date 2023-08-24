import pandas as pd

from octree import Octree
from point import Point

df = pd.read_csv('input.csv')

octree = Octree(3.0, 3.0, 3.0, Point(0.0, 0.0, 0.0))

for index, row in df.iterrows():
    octree.insert(Point(row['x'], row['y'], row['z']))

downsampled_data: [Point] = []
res_depth = 9


def downsample(node, depth):
    if node is None or len(node.children) == 0:
        return
    if depth < res_depth:
        for c in range(8):
            downsample(node.children[c], depth + 1)
    downsampled_data.extend(node.points)


downsample(octree, 0)

with open('output.csv', 'w') as file:
    file.write("x,y,z\n")
    for i in range(len(downsampled_data)):
        file.write(str(downsampled_data[i].x) + "," + str(downsampled_data[i].y) + "," + str(downsampled_data[i].z) + "\n")