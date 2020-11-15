#include <stdio.h>
#include <math.h>

int main()
{
	int bin[8] = {1,1,1,1,1,1,1,0};
	int dec = 0;
	for ( int i=1;i<=sizeof bin/sizeof bin[0];i++)
	{
		dec += bin[i-1] * pow(2,8-i);
	}
	printf("%i in binary = %i in decimal", bin, dec);
	return 0;
}
