from classes import *
import matplotlib.pyplot as plt
import numpy as np
import math
import heapq

SIZE_X = 16
SIZE_Y = 16
CANVAS_SIZE = 7
MIN_SQUARE_SIZE = 0.25

def check_collision(shape1, shape2):
    
    def check_circle_n_rectangle(point1, radius, point0):
        return (point0.x - point1.x) ** 2 + (point0.y - point1.y) ** 2 <= radius**2

    def check_dot_in_rectangle(point1, side_lenght, point0):
        return (
            point1.x <= point0.x <= point1.x + side_lenght
            or point1.x + side_lenght <= point0.x <= point1.x
        ) and (
            point1.y <= point0.y <= point1.y + side_lenght
            or point1.y + side_lenght <= point0.y <= point1.y
        )

    def get_circle_points(x0, y0, radius, step):
        points = []
        for angle in range(0, 361, step):
            t = math.radians(angle)
            x = x0 + radius * math.cos(t)
            y = y0 + radius * math.sin(t)
            points.append(Point(x, y))
        return points

    supported_shapes = [Circle,Rectangle,Line]
    if type(shape1) not in supported_shapes or type(shape2) not in supported_shapes:
        raise ValueError("Unsupported shape type")

    if isinstance(shape1, Rectangle) and isinstance(shape2, Circle):
        points = get_circle_points(shape2.x, shape2.y, shape2.radius, step=4)
        points = [
            check_dot_in_rectangle(Point(shape1.x, shape1.y), shape1.side_length, point)
            for point in points
        ]
        if (
            check_circle_n_rectangle(
                Point(shape2.x, shape2.y), shape2.radius, Point(shape1.x, shape1.y)
            )
            and check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y),
            )
            and check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x, shape1.y + shape1.side_length),
            )
            and check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y + shape1.side_length),
            )
        ):
            return 2
        elif (
            check_circle_n_rectangle(
                Point(shape2.x, shape2.y), shape2.radius, Point(shape1.x, shape1.y)
            )
            or check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y),
            )
            or check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x, shape1.y + shape1.side_length),
            )
            or check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y + shape1.side_length),
            )
            or any(points)
        ):
            return 1
        elif (
            shape1.x < shape2.x
            and shape1.y < shape2.y
            and shape1.x + shape1.side_length > shape1.x
            and shape1.y + shape1.side_length > shape2.y
            and shape1.side_length > shape2.radius
        ):
            return 2
        return 0
    else:
        raise ValueError("First needs to be as Rectangle and second is another shape")


def create_grid(all_obstacles, grid):
    flag = True
    while flag:
        flag_out = False
        flag = False
        for square in grid:
            if square.side_length == MIN_SQUARE_SIZE:
                continue
            for obstacle in all_obstacles:
                # print(check_collision(square, obstacle))
                if check_collision(square, obstacle) != 0:
                    grid.append(
                        Rectangle(
                            Point(square.x, square.y),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.append(
                        Rectangle(
                            Point(square.x + square.side_length / 2, square.y),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.append(
                        Rectangle(
                            Point(square.x, square.y + square.side_length / 2),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.append(
                        Rectangle(
                            Point(
                                square.x + square.side_length / 2,
                                square.y + square.side_length / 2,
                            ),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.remove(square)
                    flag_out = True
                    flag = True

                    break
            if flag_out:
                break

    for square in grid:
        if square.side_length == MIN_SQUARE_SIZE:
            for obstacle in all_obstacles:
                if square.color_fill == "red":
                    continue
                collision_result = check_collision(square, obstacle)
                if collision_result == 1:
                    square.color_fill = "pink"
                elif collision_result == 2:
                    square.color_fill = "red"
        else:
            square.color_fill = "white"

    return grid


def check_edges_squares(rect1, rect2):
    if rect1.x + rect1.side_length == rect2.x or rect2.x + rect2.side_length == rect1.x:
        if rect1.y >= rect2.y and rect1.y <= rect2.y + rect2.side_length:
            return True
        if rect2.y >= rect1.y and rect2.y <= rect1.y + rect1.side_length:
            return True

    if rect1.y + rect1.side_length == rect2.y or rect2.y + rect2.side_length == rect1.y:
        if rect1.x >= rect2.x and rect1.x <= rect2.x + rect2.side_length:
            return True
        if rect2.x >= rect1.x and rect2.x <= rect1.x + rect1.side_length:
            return True

    return False


def connect_neighbor_squares(graph, grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if check_edges_squares(grid[i], grid[j]) and (
                grid[i].color_fill == "white" and grid[j].color_fill == "white"
            ):
                graph.add_edge(i, j)


def sorting_key(rectangle):
    color_order = {"white": 0, "pink": 1, "red": 2}
    return color_order[rectangle.color_fill]


def check_dot_in_rectangle(point1, side_lenght, point0):
    return (
        point1.x <= point0.x <= point1.x + side_lenght
        or point1.x + side_lenght <= point0.x <= point1.x
    ) and (
        point1.y <= point0.y <= point1.y + side_lenght
        or point1.y + side_lenght <= point0.y <= point1.y
    )


def plot_path(path, graph):
    for i in range(len(path) - 1):
        key = path[i]
        value = path[i + 1]
        if key in graph.points:
            if value in graph.points:
                plt.plot(
                    [graph.points[key].x, graph.points[value].x],
                    [graph.points[key].y, graph.points[value].y],
                    linestyle="solid",
                    color="red",
                )


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def dijkstra(graph, start_index, end_index):
    distances = {index: float("infinity") for index in graph.points}
    distances[start_index] = 0
    previous_vertices = {index: None for index in graph.points}
    visited = set()

    priority_queue = [(0, start_index)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        for neighbor_index in graph.edges.get(current_vertex, []):
            neighbor_point = graph.points[neighbor_index]
            distance_to_neighbor = distances[current_vertex] + distance(
                graph.points[current_vertex], neighbor_point
            )

            if distance_to_neighbor < distances[neighbor_index]:
                distances[neighbor_index] = distance_to_neighbor
                previous_vertices[neighbor_index] = current_vertex
                heapq.heappush(priority_queue, (distance_to_neighbor, neighbor_index))

    path = []
    current_index = end_index
    while previous_vertices[current_index] is not None:
        path.insert(0, current_index)
        current_index = previous_vertices[current_index]

    path.insert(0, start_index)

    return path


def total_distance(path, graph):
    total_distance = 0
    for i in range(len(path) - 1):
        index = path[i]
        jindex = path[i + 1]
        if index in graph.points and jindex in graph.points:
            point1 = graph.points[index]
            point2 = graph.points[jindex]
            total_distance += distance(point1, point2)

    return total_distance


def mark_up_grid_n_graph(grid,graph,point_start, point_end):
    start_flag = True
    end_flag = True


    for i in range(len(grid)):
        if grid[i].color_fill == "white":
            if start_flag and check_dot_in_rectangle(
                Point(grid[i].x, grid[i].y), grid[i].side_length, point_start
            ):
                graph.add_vertex(
                    index=i,
                    point=Point(
                        grid[i].x + grid[i].side_length / 2,
                        grid[i].y + grid[i].side_length / 2,
                        color="red",
                        delta=grid[i].side_length / 2,
                    ),
                )
                start_flag = False
            elif end_flag and check_dot_in_rectangle(
                Point(grid[i].x, grid[i].y), grid[i].side_length, point_end
            ):
                graph.add_vertex(
                    index=i,
                    point=Point(
                        grid[i].x + grid[i].side_length / 2,
                        grid[i].y + grid[i].side_length / 2,
                        color="orange",
                        delta=grid[i].side_length / 2,
                    ),
                )
                end_flag = False
            else:
                graph.add_vertex(
                    index=i,
                    point=Point(
                        grid[i].x + grid[i].side_length / 2,
                        grid[i].y + grid[i].side_length / 2,
                        color="green",
                        delta=grid[i].side_length / 2,
                    ),
                )
