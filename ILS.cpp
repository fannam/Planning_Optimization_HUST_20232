#include <bits/stdc++.h>
using namespace std;

int totalNeeds = 0;
int M, N;
int totalDistance = 0;

void printVector(const vector<int>& path) {
    for (int v : path) {
        cout << v << " ";
    }
    cout << endl;
}

double calculatePercentageOfNeedsNext(const vector<int>& collected, const vector<int>& q, const vector<vector<int>>& Q, int next) {
    double total = 0;
    for (int i = 1; i <= N; i++) {
        int tmp = min(collected[i] + Q[i][next], q[i]);
        total += tmp;
    }
    return (total * 1.0) / totalNeeds;
}

double calculatePercentageOfNeeds(const vector<int>& collected, const vector<int>& q) {
    double total = 0;
    for (int i = 1; i <= N; i++) {
        int tmp = min(collected[i], q[i]);
        total += tmp;
    }
    return (total * 1.0) / totalNeeds;
}

int findNextShelf(const vector<int>& tour, const vector<int>& q, const vector<vector<int>>& Q, const vector<bool>& visited, const vector<vector<int>>& d, const vector<int>& collected) {
    int currentShelf = tour.empty() ? 0 : tour.back();
    double record = -1.0;
    int bestShelf = -1;
    for (int i = 1; i <= M; i++) {
        if (!visited[i]) {
            double newPercentage = calculatePercentageOfNeedsNext(collected, q, Q, i);
            double tmp = newPercentage / (d[currentShelf][i]);
            if (tmp > record) {
                record = tmp;
                bestShelf = i;
            }
        }
    }
    return bestShelf;
}

void solve(vector<int>& tour, const vector<int>& q, const vector<vector<int>>& Q, vector<bool>& visited, const vector<vector<int>>& d, vector<int>& collected) {
    while (calculatePercentageOfNeeds(collected, q) < 1.0) {
        int currentShelf = tour.empty() ? 0 : tour.back();
        int nextShelf = findNextShelf(tour, q, Q, visited, d, collected);
        if (nextShelf == -1) break; // No more shelves to visit
        tour.push_back(nextShelf);
        for (int i = 1; i <= N; i++) {
            collected[i] += Q[i][nextShelf];
        }
        visited[nextShelf] = true;
        totalDistance += d[currentShelf][nextShelf];
    }
    if (!tour.empty()) {
        totalDistance += d[tour.back()][0];
    }
}

int calculateTotalDistance(const vector<int>& tour, const vector<vector<int>>& d) {
    int totalDist = 0;
    int currentShelf = 0;
    for (int shelf : tour) {
        totalDist += d[currentShelf][shelf];
        currentShelf = shelf;
    }
    totalDist += d[currentShelf][0]; // Return to the starting point
    return totalDist;
}

vector<int> twoOpt(const vector<int>& tour, const vector<vector<int>>& d, int& totalDistance) {
    vector<int> bestTour = tour;
    int bestDistance = totalDistance;

    bool improvement = true;
    while (improvement) {
        improvement = false;
        for (size_t i = 0; i < bestTour.size() - 3; ++i) {
            for (size_t k = i + 2; k < bestTour.size() - 1; ++k) {
                int delta = -d[bestTour[i]][bestTour[i+1]] - d[bestTour[k]][bestTour[k+1]]
                            + d[bestTour[i]][bestTour[k]] + d[bestTour[i+1]][bestTour[k+1]];
                if (delta < 0) {
                    reverse(bestTour.begin() + i + 1, bestTour.begin() + k + 1);
                    bestDistance += delta;
                    improvement = true;
                }
            }
        }
    }
    totalDistance = bestDistance;
    return bestTour;
}

vector<int> localSearch(const vector<int>& initialTour, const vector<vector<int>>& d, int& totalDistance) {
    return twoOpt(initialTour, d, totalDistance);
}

vector<int> perturbation(const vector<int>& tour) {
    vector<int> newTour = tour;
    int i = rand() % newTour.size();
    int j = rand() % newTour.size();
    swap(newTour[i], newTour[j]);
    return newTour;
}
int record = 1e9;
vector<int> iteratedLocalSearch(vector<int>& tour, const vector<int>& q, const vector<vector<int>>& Q, vector<bool>& visited, const vector<vector<int>>& d, vector<int>& collected, int maxIterations) {
    vector<int> bestTour = tour;
    int bestDistance = calculateTotalDistance(bestTour, d);

    for (int iteration = 0; iteration < maxIterations; ++iteration) {
        vector<int> perturbedTour = perturbation(bestTour);
        int perturbedDistance = calculateTotalDistance(perturbedTour, d);
        vector<int> newTour = localSearch(perturbedTour, d, perturbedDistance);
        int newDistance = calculateTotalDistance(newTour, d);

        if (newDistance < bestDistance) {
            bestTour = newTour;
            bestDistance = newDistance;
            record = min(record, bestDistance);
        }
    }
    return bestTour;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);

    cin >> N >> M;
    vector<int> tour;
    vector<vector<int>> Q(N + 1, vector<int>(M + 1, 0));
    vector<vector<int>> d(M + 1, vector<int>(M + 1, 0));
    vector<int> q(N + 1, 0);
    vector<int> collected(N + 1, 0);
    vector<bool> visited(M + 1, false);

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

    solve(tour, q, Q, visited, d, collected);

    // Setting the number of iterations for the iterated local search
    int maxIterations = 1000;
    vector<int> bestTour = iteratedLocalSearch(tour, q, Q, visited, d, collected, maxIterations);

    cout << bestTour.size() << endl;
    printVector(bestTour);
	//cout<<record;
    return 0;
}
