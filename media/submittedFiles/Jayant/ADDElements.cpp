#include<bits/stdc++.h>
using namespace std;
int main()
{
 int i,t,n,j,value,sum=0;
 cin>>t;
 for(i=0;i<t;i++)
 {
  sum=0;
  cin>>n;
  for(j=0;j<n;j++)
  {
   cin>>value;
   sum=sum+value;
  }
  cout<<sum<<endl;
 }
 return 0;
}