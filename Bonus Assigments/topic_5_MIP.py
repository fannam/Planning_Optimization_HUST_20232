from ortools.linear_solver import pywraplp

N, K = map(int, input().split())
d = list(map(int, input().split()))
d.insert(0, 0) 
t = []
for _ in range(N + 1):
    row = list(map(int, input().split()))
    t.append(row)


solver = pywraplp.Solver.CreateSolver("SCIP")
M = int(1e6)

X = {}#X[i,j,k] tồn tại đường đi trực tiếp từ i đến j trong lộ trình nhân viên k
U = {}#U[i,k] biến MTZ của nhân viên k

for i in range(N + 1):
    for j in range(N + 1):
        for k in range(1, K + 1):
            X[i, j, k] = solver.BoolVar(f"X[{i},{j},{k}]")

for i in range(N + 1):
    for k in range(1, K + 1):
        U[i, k] = solver.IntVar(0, N, f"U[{i},{k}]")

# Constraints
# 1. Each location is serviced by exactly one technician
for i in range(1, N + 1):
    solver.Add(sum(X[i, j, k] for j in range(N + 1) for k in range(1, K + 1)) == 1)

# 2. Flow constraints
for j in range(N + 1):
    for k in range(1, K + 1):
        solver.Add(sum(X[i, j, k] for i in range(N + 1)) == sum(X[j, i, k] for i in range(N + 1)))

# 3. No self-loops
for k in range(1, K + 1):
    for i in range(N + 1):
        solver.Add(X[i, i, k] == 0)

# 4. Start and end at the depot
for k in range(1, K + 1):
    solver.Add(sum(X[0, i, k] for i in range(1, N + 1)) == 1)
    solver.Add(sum(X[i, 0, k] for i in range(1, N + 1)) == 1)

# 5. Miller-Tucker-Zemlin constraints to eliminate subtours
for k in range(1, K + 1):
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if i != j:
                solver.Add(U[i, k] - U[j, k] + M * X[i, j, k] <= M - 1)

# 6. Total time constraints
total_time = {}
for k in range(1, K + 1):
    total_time[k] = solver.IntVar(0, M, f"total_time[{k}]")
    solver.Add(total_time[k] == sum(X[i, j, k] * t[i][j] for i in range(N + 1) for j in range(N + 1)) +
                              sum(X[i, j, k] * d[j] for i in range(N + 1) for j in range(1, N + 1)))

# Minimize the maximum time
max_time = solver.IntVar(0, M, "max_time")
for k in range(1, K + 1):
    solver.Add(max_time >= total_time[k])

solver.Minimize(max_time)
solver.set_time_limit(10000)
# Solve the problem
status = solver.Solve()

# Output the solution
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(K)
    for k in range(1, K + 1):
        cur = 0
        sol = []
        sol.append(0)
        while True:
            for i in range(N + 1):
                if X[cur, i, k].solution_value() == 1:
                    if i != 0:
                        sol.append(i)
                    cur = i
                    break
            if cur == 0:
                sol.append(cur)
                break
        print(len(sol))
        for i in sol:
            print(i, end=' ')
        print()  # To print each technician's route on a new line
else:
    print("No solution")
