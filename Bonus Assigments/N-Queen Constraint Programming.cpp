#include<bits/stdc++.h>
using namespace std;
unordered_set<int>*optionSet;
stack<pair<set<int>*, int>>st;
unordered_set<int>*res;
void initialize(int n){
	set<int>* optionSet = new set<int>[n+1];
	for(int i=1; i<=n; i++){
		for(int j=1; j<=n; j++){
			optionSet[i].insert(j);
		}
	}
	
	st.push({optionSet, 1});
}

void propagate(set<int>*optionSet, int n, int col, int row){
	for(int i=col+1; i<=n; i++){
		optionSet[i].erase(row); //erase same row options
		optionSet[i].erase(row + i - col); //erase same diagonal (top-right) options 
		optionSet[i].erase(row - i + col); //bot-right options
	}
	
}

void branching(int n, set<int>*optionSet, int col){
	if(col==n + 1) return; //stop condition

	for(int row : optionSet[col]){
		set<int>* newSet = new set<int>[n+1];

		for(int i = 0; i <= n; i++){
			//if(optionSet[i].empty()) return;
			newSet[i] = optionSet[i];//copy to a temporary set, we will solve in this set
		}

		propagate(newSet, n, col, row);//propagate constraints
		
		newSet[col] = set<int>();
		newSet[col].insert(row);
		st.push({&newSet[0], col + 1});
	}
}

void explore(int n){
	while(!st.empty()){
		
		auto stop = st.top();
		st.pop();
		//cout<<stop.second<<endl;
			
		if(stop.second == n+1){
			
			for(int i=1; i<=n; i++){
				for(auto e : stop.first[i]) cout<<e<<" ";
			}
			return;
		}
		else branching(n, stop.first, stop.second);//traverse by dfs using stack
	}
}

int main(){
	int n;
	scanf("%d", &n);//n-queen
	initialize(n);
	explore(n);
}
