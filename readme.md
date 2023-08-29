### Instructions: 

To use, run downsampler.py with an input.csv file in the same directory.
An output.csv file will be created with the downsampled data.


### Description

My implementation uses an octree to represent the point data in 3D space. 
It downsamples the point data by avaraging all the points in each node at a certain depth of the octree. 
I've chosen parameters that provide a good balance, but the optimal choice will likely be different depending on the dataset.

The algorithm to generate the octree itself is fairly efficient. It will only generate as many branches as it needs to properly represent the data. However, during point insertion, it does need to traverse each branch until it finds the correct node.
Because of this, the insertion step is the main bottleneck, while the downsampling itself is quite efficient.
Besides that, the main slowdown comes from the fact that I chose to write the program in python rather than C++. I could have used the Open3D library to do the heavy lifting, but I wanted to implement the algorithm myself.