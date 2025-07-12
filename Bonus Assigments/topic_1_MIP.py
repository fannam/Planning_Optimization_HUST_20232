from ortools.linear_solver import pywraplp
N, D, A, B= map(int, input().split())
F = []
F.append([])
for _ in range(N):
    row = list(map(int, input().split()))
    row.pop()
    F.append(row)
solver = pywraplp.Solver.CreateSolver("SCIP")

X = {}
for i in range(1, N+1):
    for j in range(1, D+1):
        for k in range(5):
            X[i,j,k] = solver.BoolVar(f"X[{i},{j},{k}]")

#1: Mỗi ngày 1 nhân viên làm nhiều nhất 1 ca
for i in range(1, N+1):
    for j in range(1, D+1):
        solver.Add(sum(X[i,j,k] for k in range(5))==1)
#2: Ngày hôm trước làm ca đêm thì hôm sau được nghỉ
#if X[i, j-1, 4]==1 then X[i, j, 0]==1
#elif j not in F[i] then X[i, j, 0]==0
for i in range(1, N+1):
    for j in range(2, D+1):
        solver.Add(X[i, j, 0]>=X[i, j-1, 4])
for i in range(1, N+1):
    for j in range(1, D+1):
        if j in F[i]:
            solver.Add(X[i, j, 0]==1)
        elif j>=2:
            solver.Add(X[i, j, 0]<=X[i, j-1, 4])
#3: Mỗi ca trong ngày có ít nhất A và nhiều nhất B nhân viên
for j in range(1, D+1):
    for k in range(1, 5):
        solver.Add(sum(X[i, j, k] for i in range(1, N+1))<=B)
        solver.Add(sum(X[i, j, k] for i in range(1, N+1))>=A)
#4: F[i] là danh sách ngày nghỉ phép
for i in range(1, N+1):
    for j in F[i]:
        solver.Add(X[i, j, 0]==1)
night_shifts = {}#số ca đêm của nhân viên i
for i in range(1, N+1):
    night_shifts[i] = solver.IntVar(0, N, f"night_shifts[{i}]")
for i in range(1, N+1):
    solver.Add(night_shifts[i]==sum(X[i, j, 4] for j in range(1, D+1)))
max_night_shifts = solver.IntVar(0, N, "max_night_shifts")
for i in range(1, N+1):
    solver.Add(max_night_shifts>=night_shifts[i])
solver.Minimize(max_night_shifts)
solver.set_time_limit(10000)
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    solution = []
    for i in range(1, N+1):
        row = []
        for j in range(1, D+1):
            for k in range(0, 5):
                if X[i,j,k].solution_value():
                    row.append(k)
        solution.append(row)
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            print(solution[i][j], end=' ')
        print()