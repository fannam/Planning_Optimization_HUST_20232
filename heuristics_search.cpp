#include <bits/stdc++.h>
using namespace std;

int N, M;
int totalNeeds = 0;

typedef struct info {
    vector<int> path;
    vector<int> collected;
    vector<bool> visited;
    int distance;
} info;

void printVector(const vector<int>& path) {
    for (int v : path) {
        cout << v << " ";
    }
    cout << endl;
}

int createRandomNumber(int M) {
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    default_random_engine generator(seed);
    uniform_int_distribution<int> distribution(1, M);
    int random_number = distribution(generator);
    return random_number;
}

int recalculateDistanceSwap(const info &tour, int i, int j, const vector<vector<int>>& d) {
    int dist = tour.distance;
    int n = tour.path.size();
    int prev_i = (i == 0) ? 0 : tour.path[i - 1];
    int cur_i = tour.path[i];
    int next_i = tour.path[i + 1];
    int prev_j = tour.path[j - 1];
    int cur_j = tour.path[j];
    int next_j = (j == n - 1) ? 0 : tour.path[j + 1];

    if (j - i >= 2) {
        dist = dist - d[prev_i][cur_i] - d[cur_i][next_i] - d[prev_j][cur_j] - d[cur_j][next_j]
               + d[prev_i][cur_j] + d[cur_j][next_i] + d[prev_j][cur_i] + d[cur_i][next_j];
    } else {
        dist = dist - d[prev_i][cur_i] - d[cur_i][cur_j] - d[cur_j][next_j]
               + d[prev_i][cur_j] + d[cur_j][cur_i] + d[cur_i][next_j];
    }

    return dist;
}

int recalculateDistanceAdd(const info &tour, int index, int shelf, const vector<vector<int>>& d) {
    int dist = tour.distance;
    int n = tour.path.size();
    int prev = (index == 0) ? 0 : tour.path[index - 1];
    int cur = shelf;
    int next = (index == n) ? 0 : tour.path[index];

    dist = dist - d[prev][next] + d[prev][cur] + d[cur][next];
    return dist;
}

void swapOperator(vector<info>& neighbors, const info &tour, const vector<vector<int>>& d) {
    int n = tour.path.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            vector<int> path = tour.path;
            swap(path[i], path[j]);
            int dist = recalculateDistanceSwap(tour, i, j, d);
            neighbors.push_back({path, tour.collected, tour.visited, dist});
        }
    }
}

void addOperator(vector<info> &neighbors, const info &tour, const vector<vector<int>>& d, const vector<vector<int>>& Q, const vector<int>& q) {
    int n = tour.path.size();
    for (int i = 1; i <= M; i++) {
        if (!tour.visited[i]) {
            for (int j = 0; j <= n; j++) {
                info neighbor = tour;
                neighbor.path.insert(neighbor.path.begin() + j, i);
                neighbor.visited[i] = true;
                neighbor.distance = recalculateDistanceAdd(tour, j, i, d);
                for (int k = 1; k <= N; k++) {
                    neighbor.collected[k] += Q[k][i];
                }
                neighbors.push_back(neighbor);
            }
        }
    }
}

double calculatePercentageOfNeeds(const info &tour, const vector<int>& q) {
    double total = 0;
    for (int i = 1; i <= N; i++) {
        int tmp = min(tour.collected[i], q[i]);
        total += tmp;
    }
    return (total*1.0)/totalNeeds;
}

double heuristicsFunction(const info &tour, const vector<int>&q, double alpha, double beta) {
    double percentage = calculatePercentageOfNeeds(tour, q);
    double distance = tour.distance;
    return alpha * distance + beta * percentage;
}

void searchByHeuristics(info &solution, const vector<vector<int>>& Q, const vector<vector<int>>& d, const vector<int>& q, double alpha, double beta) {
    int loop = 1;
    bool improve = true;
    bool isExpanding = true;

    while (improve) {
        improve = false;
        vector<info> neighbors;
        if (isExpanding) addOperator(neighbors, solution, d, Q, q);
        for (auto &neighbor : neighbors) {
            double prev_f = heuristicsFunction(solution, q, alpha, beta);
            double f = heuristicsFunction(neighbor, q, alpha, beta);
            if (f > prev_f) {
                solution = neighbor;
                //cout<<calculatePercentageOfNeeds(solution, q)<<endl;
                if (calculatePercentageOfNeeds(solution, q)==1) isExpanding = false;
                improve = true;
            }
        }
    }
}

int main() {
    cin >> N >> M;
    vector<vector<int>> Q(N + 1, vector<int>(M + 1, 0));
    vector<vector<int>> d(M + 1, vector<int>(M + 1, 0));
    vector<int> q(N + 1, 0);

    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= M; j++) {
            cin >> Q[i][j];
        }
    }

    for (int i = 0; i <= M; i++) {
        for (int j = 0; j <= M; j++) {
            cin >> d[i][j];
        }
    }

    for (int i = 1; i <= N; i++) {
        cin >> q[i];
        totalNeeds += q[i];
    }

    info solution;
    int init = createRandomNumber(M);
    solution.path = {init};
    solution.visited = vector<bool>(M + 1, false);
    solution.visited[init] = true;
    solution.distance = d[0][init] + d[init][0];
    solution.collected = vector<int>(N + 1, 0);
    for (int i = 1; i <= N; i++) {
        solution.collected[i] += Q[i][init];
    }

    searchByHeuristics(solution, Q, d, q, -1, 100000);
    cout<<solution.path.size()<<endl;
    printVector(solution.path);
    //cout << solution.distance << endl;

    return 0;
}
