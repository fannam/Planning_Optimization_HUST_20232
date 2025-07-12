from ortools.linear_solver import pywraplp

n = int(input())
a = list(map(int, input().split()))
l = list(map(int, input().split()))
k = list(map(int, input().split()))
s = list(map(int, input().split()))
b, c, d = map(int, input().split())
E, F, G = map(int, input().split())
a.insert(0, 0)
l.insert(0, 0)
k.insert(0, 0)
s.insert(0, 0)
solver = pywraplp.Solver.CreateSolver("SCIP")

X = {}
Y = {}
Z = {}
#X[i] trồng lúa ở mảnh j
for j in range(1, n+1):
    X[j] = solver.BoolVar(f"X[{j}]")
    Y[j] = solver.BoolVar(f"Y[{j}]")
    Z[j] = solver.BoolVar(f"Z[{j}]")
#1: mỗi mảnh trồng 1 loại
for j in range(1, n+1):
    solver.Add(X[j]+Y[j]+Z[j]<=1)
#2: Diện tích mỗi loại không vượt quá E,F,G tương ứng
solver.Add(sum(X[j]*a[j] for j in range(1, n+1))<=E)
solver.Add(sum(Y[j]*a[j] for j in range(1, n+1))<=F)
solver.Add(sum(Z[j]*a[j] for j in range(1, n+1))<=G)

sold = solver.IntVar(0, int(1000000), "sold")
solver.Add(sold==sum(X[i]*l[i]+Y[i]*k[i]+Z[i]*s[i] for i in range(1, n+1)))
buy = solver.IntVar(0, int(1000000), "buy")
solver.Add(buy==b*sum(X[i]*a[i] for i in range(1, n+1))+c*sum(Y[i]*a[i] for i in range(1, n+1))+d*sum(Z[i]*a[i] for i in range(1, n+1)))
profit = solver.IntVar(0, int(1000000), "profit")
solver.Add(profit==sold-buy)
solver.Maximize(profit)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(int(profit.solution_value()))