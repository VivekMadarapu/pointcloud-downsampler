import pandas as pd

from octree import Octree
from point import Point

df = pd.read_csv('input.csv')

octree = Octree(0, 0, 0, Point(10, 10, 10))

for index, row in df.iterrows():
    octree.insert(Point(row['x'], row['y'], row['z']))

