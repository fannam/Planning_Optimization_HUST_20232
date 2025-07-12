from ortools.linear_solver import pywraplp


N, K = map(int, input().split())
d = [0]
c = [0]
c1 = [0]
c2 = [0]
for i in range(N):
    tmp_d, tmp_c = map(int, input().split())
    d.append(tmp_d)
    c.append(tmp_c)
for i in range(K):
    tmp_c1, tmp_c2 = map(int, input().split())
    c1.append(tmp_c1)
    c2.append(tmp_c2)
solver = pywraplp.Solver.CreateSolver("SCIP")

X = {}

for i in range(1, N+1):
    for k in range(1, K+1):
        X[i, k] = solver.BoolVar(f"X[{i},{k}]")
#1: moi don chi duoc phuc vu boi toi da 1 xe
for i in range(1, N+1):
    solver.Add(sum(X[i, k] for k in range(1, K+1))<=1)
#2: rang buoc trong tai
for k in range(1, K+1):
    solver.Add(sum(X[i, k]*d[i] for i in range(1, N+1))>=c1[k])
    solver.Add(sum(X[i, k]*d[i] for i in range(1, N+1))<=c2[k])

total_cost = solver.IntVar(0, int(1000000), "total_cost")
solver.Add(total_cost == sum(X[i,k]*c[i] for i in range(1, N+1) for k in range(1, K+1)))
solver.Maximize(total_cost)
status = solver.Solve()
solution = [0 for _ in range(N+1)]
counter = 0
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    for i in range(1, N+1):
        for k in range(1, K+1):
            if X[i,k].solution_value():
                counter += 1
                solution[i] = k
    print(counter)
    for i in range(N+1):
        if solution[i]:
            print(i, solution[i])
        
