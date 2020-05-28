#include <iostream>
#include <vector>
using namespace std;

int main()
{
    int n;
    cin>>n;
    
    vector <int> v(n);
    for(int i=0; i<n; i++)
        cin>>v[i];

    int s=v[0];    
    for(int i=1; i<n; i++)
        s+=v[i];
        
    cout<<s<<endl;
    return 0;
}