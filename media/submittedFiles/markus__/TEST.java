/* package whatever; // don't place package name! */

import java.util.*;
import java.lang.*;
import java.io.*;

/* Name of the class has to be "Main" only if the class is public. */
public class Ideone{
	public static void main (String[] args) throws java.lang.Exception{
		Scanner sc = new Scanner(System.in);
		int t = sc.nextInt();
		while(t!=0){
			int n, sum = 10;
			n = sc.nextInt();
			for(int i=0;i<n;i++){
				int x = sc.nextInt();
				sum+=x;
			}
			System.out.println(sum);
			t=t-1;
		}
	}
}