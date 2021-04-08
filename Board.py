import random
import math
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString
from Point import Point


class Board:

    def __init__(self, width=0, height=0):
        self.__width = width
        self.__height = height
        self.__points = []
        self.__links = []

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points

    @property
    def links(self):
        return self.__links

    @links.setter
    def links(self, links):
        self.__links = links

    # makes n random points on board
    def make_points(self, n):
        points_to_make = n
        while n > 0:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            p = Point(x, y)
            if p not in self.points:
                self.points.append(p)
                n -= 1

    # checks if link doesn't intersect others
    def is_link_forbidden(self, link_to_check):
        for link in self.links:
            if link[0] not in link_to_check and link[1] not in link_to_check:
                connection_1 = LineString([(link[0].x, link[0].y), (link[1].x, link[1].y)])
                connection_2 = LineString([(link_to_check[0].x, link_to_check[0].y), (link_to_check[1].x, link_to_check[1].y)])
                if connection_1.intersects(connection_2):
                    return True
        return False

    # generates links
    def make_links(self):
        # dictionary of possible end points of links
        dist = {}
        for point in self.points:
            dist[point] = []
            for point2 in self.points:
                if point != point2:
                    dist[point].append(point2)

        # sort by distance from start point
        for key, value in dist.items():
            value = sorted(value, key=lambda p: math.dist([p.x, p.y], [point.x, point.y]))

        # while there is any option to make
        while not all(value == [] for value in dist.values()):
            point = random.choice(self.points)
            if dist[point]:
                point_to_connect = dist[point][0]
                link = (point, point_to_connect)
                if not self.is_link_forbidden(link):
                    self.links.append(link)
                # delete from possible end points
                dist[point].remove(point_to_connect)
                dist[point_to_connect].remove(point)

    def draw_board(self, solution):
        plt.clf()
        x_frame = np.array([0, 0, self.width, self.width, 0])
        y_frame = np.array([0, self.height, self.height, 0, 0])
        plt.plot(x_frame, y_frame, linestyle='dashed')

        for point, color in solution.items():
            plt.plot(point.x, point.y, marker='o', color=color, ms=10)

        for link in self.links:
            x_links = np.array([link[0].x, link[1].x])
            y_links = np.array([link[0].y, link[1].y])

            plt.plot(x_links, y_links, color="black")

        plt.grid()
        plt.draw()
        plt.waitforbuttonpress(0)

    def __str__(self):
        return "WIDTH: " + str(self.width) + "\nHEIGHT: " + str(self.height) + "\nLINKS: " + str(self.links)
