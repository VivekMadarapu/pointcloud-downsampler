from point import Point


class Octree:
    def __init__(self, l, w, h, c: Point):
        self.divided = False
        self.length = l
        self.width = w
        self.height = h
        self.capacity = 1
        self.center = Point(c.x, c.y, c.z)
        self.points: [Point] = []
        self.children: [Octree] = []

    def contains(self, p):
        contains = False
        if (p.x <= self.center.x + self.length) and (p.x >= self.center.x - self.length) and (
                p.y <= self.center.y + self.width) and (p.y >= self.center.y - self.width) and (
                p.z <= self.center.z + self.height) and (p.z >= self.center.z - self.height):
            contain = True
        return contains

    def subdivide(self):
        temp = Octree(self.length / 2, self.width / 2, self.height / 2, Point(0, 0, 0))

        for i in range(8):
            if (i & 0x01):
                temp.center.x = self.center.x - temp.length
            else:
                temp.center.x = self.center.x + temp.length
            if ((i & 0x02) >> 1):
                temp.center.y = self.center.y - temp.width
            else:
                temp.center.y = self.center.y + temp.width
            if ((i & 0x04) >> 2):
                temp.center.z = self.center.z - temp.height
            else:
                temp.center.z = self.center.z + temp.height

            self.children[i] = temp
            self.divided = True

    def insert(self, p):
        if not self.contains(p):
            return False

        if len(self.points) < self.capacity:
            self.points.append(p)
            return True
        else:
            if not self.divided:
                self.subdivide()

            for i in range(8):
                inserted = self.children[i].insert(p)
                if inserted:
                    return True

        return False
