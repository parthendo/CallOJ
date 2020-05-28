#include<stdio.h>
int main()
{
    int t,i,n,j,value,sum=0;
    scanf("%d",&t);
    for(i=0;i<t;i++)
    {
        sum=0;
        scanf("%d",&n);
        for(j=0;j<n;j++)
        {
            scanf("%d",&value);
            sum=sum+value;
        }
        printf("%d\n",sum);
    }
}