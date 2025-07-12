from ortools.linear_solver import pywraplp

N, M = map(int, input().split())
d = list(map(int, input().split()))
d.insert(0, 0)
c = list(map(int, input().split()))
c.insert(0, 0)
K = int(input())
conflict = []
for _ in range(K):
    row = list(map(int, input().split()))
    conflict.append(row)

solver = pywraplp.Solver.CreateSolver("SCIP")

X = {}#Lớp i được phân vào phòng j kíp k (k=1,...,N)
for i in range(1, N+1):
    for j in range(1, M+1):
        for k in range(1, N+1):
            X[i,j,k] = solver.BoolVar(f"X[{i},{j},{k}]")
#constraint 1: Mỗi lớp chỉ được xếp lịch 1 lần
for i in range(1, N+1):
    solver.Add(sum(X[i,j,k] for j in range(1, M+1) for k in range(1, N+1))==1)
#constraint 2: Mỗi phòng thi chỉ được xếp cho tối đa 1 lớp trong 1 kíp thi
for j in range(1, M+1):
    for k in range(1, N+1):
        solver.Add(sum(X[i,j,k] for i in range(1, N+1))<=1)
#constraint 3: 2 lớp conflict không được xếp chung kíp thi
for (i1, i2) in conflict:
    i1 = int(i1)
    i2 = int(i2)
    for k in range(1, N+1):
        solver.Add(sum(X[i1, j, k] + X[i2, j, k] for j in range(1, M+1)) <= 1)
#constraint 4: Số chỗ trong phòng thi phải >= số sinh viên của lớp được xếp
for i in range(1, N+1):
    for j in range(1, M+1):
        for k in range(1, N+1):
            solver.Add(X[i,j,k]*d[i]<=c[j])
#objective
max_shift = solver.IntVar(0, N, "max_shift")
for i in range(1, N+1):
    for j in range(1, M+1):
        for k in range(1, N+1):
            solver.Add(max_shift>=X[i,j,k]*k)
solver.Minimize(max_shift)
solver.set_time_limit(10000)
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(max_shift.solution_value())
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            for k in range(1, N + 1):
                if X[i, j, k].solution_value():
                    print(i, j, k)
else:
    print('No solution found.')
        
    
