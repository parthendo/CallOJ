#include <iostream>
#include <vector>
using namespace std;

int main()
{
    int n, k;
    cin>>n>>k;
    
    int arr[n+5];
    for(int i=0;i<n;i++){
        cin>>arr[i];
    }
    int flag = -1;
    for(int i=0;i<n;i++){
        if(arr[i] == k) flag = 1;
    }
    cout << flag;
    
    return 0;
}