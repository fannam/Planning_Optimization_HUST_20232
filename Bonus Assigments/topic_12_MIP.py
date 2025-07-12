from ortools.linear_solver import pywraplp

# Định nghĩa giá trị vô cùng lớn và các hằng số
INF_POSITIVE = int(1000000)
INF_NEGATIVE = int(-1000000)
M = int(1000000)

# Đọc vào dữ liệu từ người dùng
N = int(input())
e = [0]
l = [0]
d = [0]
for i in range(1, N+1):
    tmp_e, tmp_l, tmp_d = map(int, input().split())
    e.append(tmp_e)
    l.append(tmp_l)
    d.append(tmp_d)

t = []
for i in range(0, N+1):
    row = list(map(int, input().split()))
    t.append(row)

# Khởi tạo solver
solver = pywraplp.Solver.CreateSolver("SCIP")

# Khởi tạo các biến quyết định
X = {}  # Tồn tại đường đi trực tiếp từ i -> j trong lời giải
Y = {}  # Thời gian bắt đầu giao hàng tại điểm i
U = {}  # Biến loại bỏ subtour
for i in range(0, N+1):
    for j in range(0, N+1):
        X[i, j] = solver.BoolVar(f"X[{i},{j}]")
for i in range(0, N+1):
    Y[i] = solver.IntVar(INF_NEGATIVE, INF_POSITIVE, f"Y[{i}]")
    U[i] = solver.IntVar(0, N+1, f"U[{i}]")

# Các ràng buộc:
# 1: Mỗi điểm chỉ được thăm chính xác 1 lần
for i in range(1, N+1):
    solver.Add(sum(X[i, j] for j in range(0, N+1) if i != j) == 1)
    solver.Add(sum(X[j, i] for j in range(0, N+1) if i != j) == 1)
    solver.Add(X[i, i] == 0)

# 2: Bắt đầu tại kho (0), kết thúc tại kho (0)
solver.Add(sum(X[0, i] for i in range(1, N+1)) == 1)
solver.Add(sum(X[i, 0] for i in range(1, N+1)) == 1)

# 3: Ràng buộc loại bỏ subtour (Miller Tucker Zemlin)
for i in range(1, N+1):
    for j in range(1, N+1):
        if i != j:
            solver.Add(U[i] - U[j] + M * X[i, j] <= M - 1)

# 4: Ràng buộc thời gian giao hàng
for i in range(0, N+1):
    for j in range(1, N+1):
        if i != j:
            solver.Add(Y[j] >= Y[i] + d[i] + t[i][j] - M * (1 - X[i, j]))

# 5: Ràng buộc thời gian phục vụ trong khoảng cho phép
for i in range(1, N+1):
    solver.Add(Y[i] >= e[i])
    solver.Add(Y[i] <= l[i])

# Hàm mục tiêu: Tổng thời gian di chuyển
move_time = solver.IntVar(0, M, "move_time")
solver.Add(move_time == sum(X[i, j] * t[i][j] for i in range(0, N+1) for j in range(0, N+1)))
solver.Minimize(move_time)

# Giải bài toán
status = solver.Solve()

# In kết quả
solution = []
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(N)
    cur = 0
    while True:
        for i in range(N+1):
            if X[cur, i].solution_value():
                solution.append(i)
                cur = i
                break
        if cur==0:
            break
    solution.pop()
    for i in range(len(solution)):
        print(solution[i], end=' ')
                
else:
    print("No solution found")
