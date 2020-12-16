#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <locale.h>
#include <wchar.h>
#include <math.h>
#define n 150
int loop();
int binToDec(int e[n]);
int bits[n];
int newbits[n];
int main()
{
	srand((unsigned) time(NULL));
	setlocale(LC_CTYPE, "");
	// Initialisation of arrays:
	for(int i=0;i<n;i++)
	{
		bits[i]=0;
		newbits[i]=0;
		bits[i] = rand() % 2;
	}
	bits[n/2]=1;
	bits[3*n/4]=1;
	for(int i=0;i<n;i++)
	{
		printf("%s",bits[i]?".":" ");
	}
	printf("\n");
	// Looping the function for k generations:
	int k = 100;
	for(int i=0;i<k;i++)
	{
		loop();
		usleep(50000);
	}
	return 0;
}
int loop()
{
	for(int i=0;i<n;i++)
	{
		if(i==n){bits[n+1]=0;}
		// newbits[i] = bits[i-1] ^ (bits[i] | bits[i+1]); 	// Rule 30
		// newbits[i] = bits[i-1] ^ bits[i+1]; 			// Rule 90
		
		////////////////////////////////////////////////	// Rule 110
		if (!bits[i] && bits[i+1])
		{
			newbits[i] = 1;
		}
		else if (bits[i] && bits[i-1] && bits[i+1])
		{
			newbits[i] = 0;
		}
		/////////////////////////////////////////////////	// End of Rule 110
		if(i==0){newbits[i]=0;}
	}
	int sum = 0;
	for (int i=0;i<n;i++)
	{
		wchar_t sq = 0xA1;
		bits[i] = newbits[i];
		printf("%s",bits[i]?/*"□"*/"■":" ");
	}
	printf("\n");
	// printf("%lld\n",binToDec(bits));
	return 0;
}

int binToDec(int e[n])
{
	long long dec = 0;
	for (int j=1;j<=n;j++)
	{
		dec += e[j-1]*pow(2,n-j);
	}
	return dec;
}
