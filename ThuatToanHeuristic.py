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
wn.title("A* Maze Solver")
wn.setup(1300, 700)
wn.tracer(0) 

class Cell(turtle.Turtle):
    def __init__(self, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.penup()
        self.speed(0)
        self.shapesize(22/20)

maze = Cell("white")              # tường
start_turtle = Cell("red")        # điểm bắt đầu
end_turtle = Cell("green")        # điểm kết thúc
path_turtle = Cell("lightblue")   # các ô A* duyệt qua
solution_turtle = Cell("yellow")  # đường đi ngắn nhất

walls = []
path = set()


CELL = 24
OFFSET_X = -588
OFFSET_Y = 288

start_pos = None
end_pos = None


DELAY_ASTAR = 0.1 
DELAY_SOLUTION = 0.1 

def setup_maze(grid):
    global start_pos, end_pos
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            screen_x = OFFSET_X + x * CELL
            screen_y = OFFSET_Y - y * CELL

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

def h(node, goal):
    return abs((node[0] - goal[0]) // CELL) + abs((node[1] - goal[1]) // CELL)


def draw_solution(parent, start, goal):
    print("\nVẽ đường đi ngắn nhất")
    path_nodes = []
    current = goal
    while current != start:
        path_nodes.append(current)
        current = parent[current]
    path_nodes.append(start)
    path_nodes.reverse()

    for i, pos in enumerate(path_nodes):
        if pos != start and pos != end_pos:
            solution_turtle.goto(pos)
            solution_turtle.stamp()
            wn.update()
            print(f"  Bước {i}: Đã vẽ ô tại vị trí {pos}")
            time.sleep(DELAY_SOLUTION)
    wn.update()

graph = defaultdict(list)
def A_star(graph, start, goal):
    print("\nBắt đầu thuật toán A*...")
    MO = [start]    
    DONG = []       
    g = {start: 0} 
    f = {start: h(start, goal)}
    parent = {}
    step_count = 0
    while MO:
        min_f = float('inf')
        min_node = None
        for node in MO:
            if f[node] < min_f:
                min_f = f[node]
                min_node = node
        n = min_node
        step_count += 1
        print(f"\nBước {step_count}: Đang xét ô tại vị trí {n}")
        if n != start_pos and n != end_pos:
            path_turtle.goto(n)
            path_turtle.stamp()
            wn.update()
            print(f"  Đã vẽ ô màu xanh lam tại {n}")
            time.sleep(DELAY_ASTAR)
        if n == goal:
            print("\nTìm thấy điểm kết thúc!")
            print(f"  Tổng số bước đã duyệt: {step_count}")
            draw_solution(parent, start, goal)
            return True
        MO.remove(n)
        DONG.append(n)
        neighbors = graph.get(n, [])
        print(f"  Có {len(neighbors)} ô lân cận có thể đi")
        for m in neighbors:
            tentative_g = g[n] + 1 
            if m not in MO and m not in DONG:
                g[m] = tentative_g
                f[m] = g[m] + h(m, goal)
                parent[m] = n
                MO.append(m)
                print(f"    Thêm ô {m} vào hàng đợi, g={g[m]}, h={h(m, goal)}, f={f[m]}")
            elif m in MO and tentative_g < g[m]:
                g[m] = tentative_g
                f[m] = g[m] + h(m, goal)
                parent[m] = n
                print(f"    Cập nhật ô {m} trong hàng đợi, g={g[m]}, h={h(m, goal)}, f={f[m]}")

    print("\nKhông tìm thấy đường đi đến điểm kết thúc.")
    return False

def main():
    print("BẮT ĐẦU CHƯƠNG TRÌNH GIẢI MÊ CUNG BẰNG A*")
    setup_maze(GRID)

    print("\nThông tin mê cung:")
    print(f"  - Điểm bắt đầu (màu đỏ): {start_pos}")
    print(f"  - Điểm kết thúc (màu xanh lá): {end_pos}")
    print(f"  - Tổng số ô có thể đi: {len(path)}")

    start_time = time.time()
    success = A_star(graph, start_pos, end_pos)
    elapsed_time = time.time() - start_time
    print(f"\nThời gian chạy A*: {elapsed_time:.4f} giây")

    if success:
        print("\nGIẢI MÊ CUNG THÀNH CÔNG!")
    else:
        print("\nKHÔNG THỂ TÌM ĐƯỜNG ĐI!")

    print("=" * 50)

if __name__ == "__main__":
    main()
    wn.exitonclick()