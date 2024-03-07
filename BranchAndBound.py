#M cái kệ, N sản phẩm
#Q[i][j] là số sản phẩm loại i ở kệ j 
#Nhân viên bắt đầu đi từ cửa (điểm 0) của nhà kho và muốn thăm một vài cái kệ nào đó
#Mỗi cái kệ chỉ được thăm tối đa 1 lần 
#Nhân viên quay trở lại cửa (điểm 0) sau khi đã lấy đủ các sản phẩm theo yêu cầu khách hàng
#q[i] là số lượng sản phẩm loại i mà nhân viên đó phải lấy
#d(i,j) là ma trận khoảng cách từ i tới j (1<=i,j<=M)
#Hàm mục tiêu: Khoảng cách nhỏ nhất cần phải đi

#dòng 1: Nhập N và M
#dòng 1+i: dòng i của ma trận Q
#dòng N+i+2: dòng i của ma trận khoảng cách d
#dòng N+M+3: giá trị vector q

#X[i] là vị trí của người nhân viên tại bước thứ i (1<=i<=N, X[0]=0)
#constraint:
#Mỗi cái kệ chỉ được thăm tối đa 1 lần (X[i] != X[j] với mọi 1<=i<j)
#Nhân viên quay trở lại điểm 0 thì kết thúc (if X[i]==0 and i>1 then END)
#sigma (k in route) Q[i][k] >= q[i] với mọi i=1...N
#hàm mục tiêu: min (sigma(i=0->len(route)-1) d(X[i], X[i+1])) (với X[route]=0)

def post_check(q, capacity):
    for i in range(0, N):
        if capacity[i]<q[i]:
            return False
    return True 

def TRY(X, M, N, k):
    global visited, Q, q, d, capacity, current_distance, current_record, solution
    for value in range(1, M+1):
        if not visited[value]:
            X[k] = value
            visited[value] = True
            current_distance += d[X[k-1]][value]
            for i in range(1, N+1):
                capacity[i-1] += Q[i][value]
            if k==M and not post_check(q, capacity):
                print(-1)
            elif post_check(q, capacity):
                print(current_distance+d[value][0])
                print(X)
                
                if current_distance + d[value][0] < current_record:
                    current_record = current_distance + d[value][0]
                    solution = []
                    for element in X:
                        if element!=0:
                            solution.append(element)
            else:
                if current_distance < current_record:
                    TRY(X, M, N, k+1)
            X[k] = 0
            visited[value] = False
            current_distance -= d[X[k-1]][value]
            for i in range(1, N+1):
                capacity[i-1] -= Q[i][value]
    
def solve(M, N):
    global solution
    X = [0 for _ in range(M+1)]
    TRY(X, M, N, 1)
    print(len(solution))
    for x in solution:
        print(x, end=' ')

txt = input()
numbers = txt.split()
N = int(numbers[0])
M = int(numbers[1])
Q = [[0]*(M+1) for _ in range(N+1)]
d = []
visited = [False]*(M+1)
capacity = [0 for _ in range(N+1)]
current_distance = 0
current_record = float('inf')
solution = []

for i in range(1, N + 1):
    row = input()
    row_elements = [int(x) for x in row.split()]
    # Cập nhật giá trị cho từng phần tử trong hàng
    for j in range(1, M + 1):
        Q[i][j] = row_elements[j - 1]
for i in range(M+1):
    row = input()
    row_elements = [int(x) for x in row.split()]
    d.append(row_elements)
row = input()
q = [int(x) for x in row.split()]
solve(M, N)
