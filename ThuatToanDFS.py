import turtle
from collections import defaultdict
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
wn.title("DFS Maze Solver")
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

class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent

maze = Cell("white")
start_turtle = Cell("red")
end_turtle = Cell("green")
path_turtle = Cell("lightblue")
solution_turtle = Cell("yellow")

walls = []
path = set()
graph = defaultdict(list)

CELL = 24
DiemDau = -588
DiemCuoi = 288

start_pos = None
end_pos = None

DELAY_DFS = 0.1
DELAY_SOLUTION = 0.1


def MeCung(grid):
    global start_pos, end_pos
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            screen_x = DiemDau + x * CELL
            screen_y = DiemCuoi - y * CELL

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
        for dx, dy in [(-CELL, 0), (CELL, 0), (0, -CELL), (0, CELL)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in path:
                graph[(x, y)].append((nx, ny))


def draw(node):
    print("\nVẽ đường đi tìm được")
    path_nodes = []
    while node:
        path_nodes.append(node.pos)
        node = node.parent

    for i, pos in enumerate(reversed(path_nodes)):
        if pos != start_pos and pos != end_pos:
            solution_turtle.goto(pos)
            solution_turtle.stamp()
            wn.update()
            print(f"  Bước {i+1}: Đã vẽ ô tại vị trí {pos}")
            time.sleep(DELAY_SOLUTION)
    wn.update()


def DFS(start, goal):
    frontier = [Node(start)]
    visited = set([start])
    solution_node = None
    step_count = 0

    while frontier:
        current = frontier.pop()
        step_count += 1
        print(f"\nBước {step_count}: Đang xét ô tại vị trí {current.pos}")

        if current.pos != start_pos and current.pos != end_pos:
            path_turtle.goto(current.pos)
            path_turtle.stamp()
            wn.update()
            print(f"  Đã vẽ ô màu xanh lam tại {current.pos}")
            time.sleep(DELAY_DFS)

        if current.pos == goal:
            solution_node = current
            print("\nTìm thấy điểm kết thúc!")
            print(f"  Tổng số bước đã duyệt: {step_count}")
            break

        neighbors = graph[current.pos]
        print(f"  Có {len(neighbors)} ô lân cận có thể đi")

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(Node(neighbor, parent=current))


    wn.update()
    time.sleep(1)

    if solution_node:
        draw(solution_node)
        return True
    else:
        print("\nKhông tìm thấy đường đi đến điểm kết thúc.")
        return False


def main():
    print("BẮT ĐẦU CHƯƠNG TRÌNH GIẢI MÊ CUNG BẰNG DFS")

    MeCung(GRID)

    print("\nThông tin mê cung:")
    print(f"  - Điểm bắt đầu (màu đỏ): {start_pos}")
    print(f"  - Điểm kết thúc (màu xanh lá): {end_pos}")
    print(f"  - Tổng số ô có thể đi: {len(path)}")

    time.sleep(1)

    start_time = time.time()
    success = DFS(start_pos, end_pos)
    elapsed_time = time.time() - start_time
    print(f"\nThời gian chạy DFS: {elapsed_time:.4f} giây")

    if success:
        print("\nGIẢI MÊ CUNG THÀNH CÔNG!")
    else:
        print("\nKHÔNG THỂ TÌM ĐƯỜNG ĐI!")

    print("=" * 50)


if __name__ == "__main__":
    main()
    wn.exitonclick()