#include <iostream>

int main(){
    int t; cin >> t;
    while(t--){
      int sum = 0, n;
      cin >> n;
      for(int i=0;i<n;i++){
       int x;  cin >> x;
      sum+=x;
      }
     cout << sum << endl;
    }
    return 0;
}