#include <bits/stdc++.h>
using namespace std;

int main(){

  int t;
  cin >> t;
  while(t--){
    int n, sum = 0;
    int arr[10];
    cin >> n;
    arr[1] = n;
    n = arr[100];
    for(int i=0;i<n;i++){
      int x;  cin >> x;
      sum+=x;
    }
    cout << sum << endl;
  }
  return 0;
}
