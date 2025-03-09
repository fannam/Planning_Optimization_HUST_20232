from ortools.sat.python import cp_model

model = cp_model.CpModel()

N, M = map(int, input().split())
Q = [[0] * (M + 1)]
for _ in range(N):
    row = list(map(int, input().split()))
    Q.append([0] + row)
d = [list(map(int, input().split())) for _ in range(M+1)]
q = list(map(int, input().split()))

#Variables
X = {}
for i in range(M+1):
    for j in range(M+1):
        X[i, j] = model.NewBoolVar(f'X[{i},{j}]')
#Helper variables
U = {}
for i in range(1, M + 1):
    U[i] = model.NewIntVar(1, M, f'U[{i}]')

#Constraints
#No.1: Each shelf is visited exactly once (outgoing and incoming)
for i in range(M + 1):
    model.Add(sum(X[i, j] for j in range(M+1)) <= 1)  # Outgoing from i
    model.Add(sum(X[j, i] for j in range(M+1)) <= 1)  # Incoming to i
    model.Add(X[i, i] == 0)  # No self-loops

#No.2: If a shelf is visited, it must be left exactly once
for j in range(1, M + 1):
    model.Add(sum(X[i, j] for i in range(M+1)) == sum(X[j, k] for k in range(M+1)))

#No.3: Required quantities must be met
for i in range(1, N + 1):
    model.Add(sum(Q[i][j]*sum(X[k, j] for k in range(M+1)) for j in range(1, M+1)) >= q[i-1])

#Addition constraint for No.1: Sub-tour elimination constraints
for i in range(1, M + 1):
    for j in range(1, M + 1):
        if i != j:
            model.Add(U[i]-U[j]+M*(X[i, j]-1) <= - 1)
#No.5: Start from 0, end at 0
model.Add(sum(X[0, j] for j in range(1, M+1)) == 1)
model.Add(sum(X[j, 0] for j in range(1, M+1)) == 1)

total_distance = model.NewIntVar(0, sum(sum(row) for row in d), 'total_distance')
model.Add(total_distance == sum(X[i, j]*d[i][j] for i in range(M+1) for j in range(M+1)))

model.Minimize(total_distance)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    cur = 0
    sol = []
    while True:
        for i in range(M + 1):
            if solver.Value(X[cur, i]) == 1:
                if i != 0:
                    sol.append(i)
                cur = i
                break
        if cur == 0:
            break
    print(len(sol))
    for i in sol:
        print(i, end=' ')
else:
    print(-1)
