from ortools.linear_solver import pywraplp

N, M, b = map(int, input().split())
L = [[0]]
for i in range(N):
    row = list(map(int, input().split()))
    row.pop(0)
    L.append(row)
#print(L)
solver = pywraplp.Solver.CreateSolver("SCIP")

X = {}
for i in range(1, M+1):
    for j in range(1, N+1):
        X[i,j] = solver.BoolVar(f"X[{i},{j}]")
for j in range(1, N+1):
    for i in range(1, M+1):
        if i not in L[j]:
            solver.Add(X[i,j]==0)
for j in range(1, N+1):
    solver.Add(sum(X[i, j] for i in range(1, M+1))==b)

load = {}
for i in range(1, M+1):
    load[i] = solver.IntVar(0, N, f"load[{i}]")
for i in range(1, M+1):
    solver.Add(load[i]==sum(X[i,j] for j in range(1, M+1)))
max_load = solver.IntVar(0, N, "max_load")
for i in range(1, M+1):
    solver.Add(max_load>=load[i])
solver.Minimize(max_load)
status = solver.Solve() 
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(N)
    for j in range(1, N + 1):
        assigned_reviewers = [i for i in range(1, M + 1) if X[i, j].solution_value()]
        print(b, ' '.join(map(str, assigned_reviewers)))
else:
    print('No solution found.')
