import matplotlib.pyplot as plt
import numpy as np

class Graph:
    def __init__(self):
        self.edges = {}
        self.points = {}

    def add_vertex(self, point, index):
        index = len(self.points)
        self.points[index] = point

    def add_edge(self, index, jindex):
        if index in self.edges:
            if jindex not in self.edges[index]:
                self.edges[index].append(jindex)
        else:
            self.edges[index] = [jindex]

    def plot_dots(self):
        for point in self.points.values():
            point.plot()

    def plot_edges(self):
        for key, values in self.edges.items():
            if key in self.points:
                for value in values:
                    if value in self.points:
                        plt.plot(
                            [self.points[key].x, self.points[value].x],
                            [self.points[key].y, self.points[value].y],
                            linestyle="--",
                            color="blue",
                            alpha=0.1,
                        )

    def plot_neighbors(self, index):
        for value in self.edges[index]:
            plt.plot(
                [self.points[index].x, self.points[value].x],
                [self.points[index].y, self.points[value].y],
                linestyle="solid",
                color="red",
            )


class Point:
    def __init__(self, x, y, label=None, color="black", delta=None):
        self.x = x
        self.y = y
        self.label = label
        self.color = color
        self.delta = delta

    def plot(self):
        plt.scatter(self.x, self.y, color=self.color)
        if self.label is not None:
            plt.text(self.x, self.y, self.label, fontsize=12, ha="center")


class Line:
    def __init__(self, start_point, end_point, color="black", marker=None):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.marker = marker

    def plot(self):
        plt.plot(
            [self.start_point.x, self.end_point.x],
            [self.start_point.y, self.end_point.y],
            marker=self.marker,
            color=self.color,
        )


class Rectangle:
    def __init__(
        self, point, side_length, color_border="black", color_fill="white", marker=None
    ):
        self.x = point.x
        self.y = point.y
        self.side_length = side_length
        self.color_border = color_border
        self.color_fill = color_fill
        self.marker = marker

    def plot(self,):
        plt.fill(
            [self.x, self.x + self.side_length, self.x + self.side_length, self.x],
            [self.y, self.y, self.y + self.side_length, self.y + self.side_length],
            color=self.color_fill,
        )
        plt.plot(
            [
                self.x,
                self.x + self.side_length,
                self.x + self.side_length,
                self.x,
                self.x,
            ],
            [
                self.y,
                self.y,
                self.y + self.side_length,
                self.y + self.side_length,
                self.y,
            ],
            color=self.color_border,
            marker=self.marker,
        )


class Circle:
    def __init__(
        self, point, radius, color_fill="black", color_border="black", marker=None
    ):
        self.x = point.x
        self.y = point.y
        self.radius = radius
        self.color_fill = color_fill
        self.color_border = color_border
        self.marker = marker

    def plot(self):
        circle = plt.Circle(
            (self.x, self.y), self.radius, color=self.color_fill, fill=True
        )
        plt.gca().add_patch(circle)

        circle_border = plt.Circle(
            (self.x, self.y), self.radius, color=self.color_border, fill=False
        )
        plt.gca().add_patch(circle_border)
        if self.marker is not None:
            plt.scatter(*(self.x, self.y), color=self.color_border, marker=self.marker)