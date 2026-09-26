import turtle
from collections import defaultdict
import heapq
import time

GRID = [
    "+++++++++++++++++++++++++",
    "+s      +       +       +",
    "+ +++++ + +++++ + +++++ +",
    "+ +     +     + +     + +",
    "+ + +++++ +++ + + +++ + +",
    "+ +     +   + + +   + + +",
    "+ + +++++ + + + + + + + +",
    "+ +     + + + + + + + + +",
    "+ + +++ + + + + + + + + +",
    "+ + +   + + + + + + + + +",
    "+ + + +++ + + + + + + + +",
    "+ + +     + + + + + + + +",
    "+ + +++++++ + + + + + + +",
    "+       +     + + + + + +",
    "+ +++++ + +++++ + + + + +",
    "+ +     +     + + + + + +",
    "+ + +++++ +++ + + + + + +",
    "+ +     +   + + + + + + +",
    "+ + +++++ + + + + + + + +",
    "+ +     + + + + + + + + +",
    "+ + +++ + + + + + + + + +",
    "+ + +   + + + + + + + + +",
    "+ + + +++ + + + + + + + +",
    "+ +         +       +   e+",
    "+++++++++++++++++++++++++",
]

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Greedy Best-First Maze Solver")
wn.setup(1300, 700)
wn.tracer(0)

class Cell(turtle.Turtle):
    def __init__(self, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.penup()
        self.speed(0)
        self.shapesize(22 / 20)

maze = Cell("white")
start_turtle = Cell("red")
end_turtle = Cell("green")
path_turtle = Cell("lightblue")
solution_turtle = Cell("yellow")

walls = []
path = set()
graph = defaultdict(list)

cell = 24
DiemDau = -588
DiemCuoi = 288

start_pos = None
end_pos = None

DoTreTK = 0.1
DoTre = 0.1


def MeCung(grid):
    global start_pos, end_pos
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            screen_x = DiemDau + x * cell
            screen_y = DiemCuoi - y * cell

            if char == "+":
                maze.goto(screen_x, screen_y)
                maze.stamp()
                walls.append((screen_x, screen_y))
            elif char in " se":
                path.add((screen_x, screen_y))
                if char == "s":
                    start_pos = (screen_x, screen_y)
                elif char == "e":
                    end_pos = (screen_x, screen_y)

    wn.update()

    start_turtle.goto(start_pos)
    start_turtle.stamp()
    end_turtle.goto(end_pos)
    end_turtle.stamp()
    wn.update()

    for (x, y) in path:
        for dx, dy in [(-cell, 0), (cell, 0), (0, -cell), (0, cell)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in path:
                graph[(x, y)].append((nx, ny))


def heuristic(node, goal):
    return abs(node[0] - goal[0]) // cell + abs(node[1] - goal[1]) // cell


def reconstruct_path(came_from, start, goal):
    path_nodes = []
    current = goal
    while current != start:
        path_nodes.append(current)
        current = came_from[current]
    path_nodes.append(start)
    path_nodes.reverse()
    return path_nodes


def draw(path_nodes):
    print("\nVẽ đường đi tìm được")
    for i, pos in enumerate(path_nodes):
        if pos != start_pos and pos != end_pos:
            solution_turtle.goto(pos)
            solution_turtle.stamp()
            wn.update()
            print(f"  Bước {i+1}: Đã vẽ ô tại vị trí {pos}")
            time.sleep(DoTre)
    wn.update()


def Greedy(start, goal):
    open_heap = [(heuristic(start, goal), start)]
    visited = set([start])
    came_from = {}
    step_count = 0

    while open_heap:
        _, current = heapq.heappop(open_heap)
        step_count += 1
        print(f"\nBước {step_count}: Đang xét ô tại vị trí {current} với h={heuristic(current, goal)}")

        if current != start_pos and current != end_pos:
            path_turtle.goto(current)
            path_turtle.stamp()
            wn.update()
            print(f"  Đã vẽ ô màu xanh lam tại {current}")
            time.sleep(DoTreTK)

        if current == goal:
            print("\nTìm thấy điểm kết thúc!")
            print(f"  Tổng số bước đã duyệt: {step_count}")
            return reconstruct_path(came_from, start, goal)

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                heapq.heappush(open_heap, (heuristic(neighbor, goal), neighbor))
                print(f"    Thêm ô {neighbor} vào heap, h={heuristic(neighbor, goal)}")

    return None


def main():
    print("BẮT ĐẦU CHƯƠNG TRÌNH GIẢI MÊ CUNG BẰNG GREEDY BEST-FIRST")

    MeCung(GRID)

    print("\nThông tin mê cung:")
    print(f"  - Điểm bắt đầu (màu đỏ): {start_pos}")
    print(f"  - Điểm kết thúc (màu xanh lá): {end_pos}")
    print(f"  - Tổng số ô có thể đi: {len(path)}")

    time.sleep(1)

    start_time = time.time()
    solution = Greedy(start_pos, end_pos)
    elapsed_time = time.time() - start_time
    print(f"\nThời gian chạy Greedy: {elapsed_time:.4f} giây")

    if solution:
        print(f"\nĐường đi có {len(solution)} bước.")
        draw(solution)
        print("\nGIẢI MÊ CUNG THÀNH CÔNG!")
    else:
        print("\nKHÔNG THỂ TÌM ĐƯỜNG ĐI!")

    print("=" * 50)


if __name__ == "__main__":
    main()
    wn.exitonclick()