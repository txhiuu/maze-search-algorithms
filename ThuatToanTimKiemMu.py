import turtle
from collections import deque, defaultdict
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
wn.title("BFS Maze Solver")
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

class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent


maze = Cell("white")              # tường
start_turtle = Cell("red")        # điểm bắt đầu
end_turtle = Cell("green")        # điểm kết thúc
path_turtle = Cell("lightblue")   # các ô duyệt qua
solution_turtle = Cell("yellow")  # đường đi ngắn nhất

walls = []
path = set()
graph = defaultdict(list)

CELL = 24
OFFSET_X = -588
OFFSET_Y = 288

start_pos = None
end_pos = None


DELAY_BFS = 0.1   
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

    # Xây dựng đồ thị
    for (x, y) in path:
        for dx, dy in [(-CELL, 0), (CELL, 0), (0, -CELL), (0, CELL)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in path:
                graph[(x, y)].append((nx, ny))


def draw_solution(node):
    print("\nVẽ đường đi ngắn nhất")
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

def BFS(start, goal):
    frontier = deque([Node(start)])
    visited = set([start])
    solution_node = None
    step_count = 0
    while frontier:
        current = frontier.popleft()
        step_count += 1     
        print(f"\nBước {step_count}: Đang xét ô tại vị trí {current.pos}")
        if current.pos != start_pos and current.pos != end_pos:
            path_turtle.goto(current.pos)
            path_turtle.stamp()
            wn.update()
            print(f"  Đã vẽ ô màu xanh lam tại {current.pos}")
            time.sleep(DELAY_BFS)  
        
        if current.pos == goal:
            solution_node = current
            print("\nTìm thấy điểm kết thúc!")
            print(f"  Tổng số bước đã duyệt: {step_count}")
            break   
        # Kiểm tra các ô lân cận
        neighbors = graph[current.pos]
        print(f"  Có {len(neighbors)} ô lân cận có thể đi")
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(Node(neighbor, parent=current))
                print(f"    Thêm ô {neighbor} vào hàng đợi")
    wn.update()
    time.sleep(1) 

    if solution_node:
        draw_solution(solution_node)
        return True
    else:
        print("\nKhông tìm thấy đường đi đến điểm kết thúc.")
        return False

def main():
    print("BẮT ĐẦU CHƯƠNG TRÌNH GIẢI MÊ CUNG BẰNG BFS")
    
    setup_maze(GRID)
    
    print("\nThông tin mê cung:")
    print(f"  - Điểm bắt đầu (màu đỏ): {start_pos}")
    print(f"  - Điểm kết thúc (màu xanh lá): {end_pos}")
    print(f"  - Tổng số ô có thể đi: {len(path)}")
    
    time.sleep(1) 
    
    # Đo thời gian chạy BFS
    start_time = time.time()
    success = BFS(start_pos, end_pos)
    elapsed_time = time.time() - start_time
    print(f"\nThời gian chạy BFS: {elapsed_time:.4f} giây")
    
    if success:
        print("\nGIẢI MÊ CUNG THÀNH CÔNG!")
    else:
        print("\nKHÔNG THỂ TÌM ĐƯỜNG ĐI!")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
    wn.exitonclick()