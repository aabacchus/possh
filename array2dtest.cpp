#include <stdio.h>
#include <iostream>

int x[2][3];
int main(){
for(int i=0;i<3;i++){
	x[0][i]=i+10;
}
std::cout<<x[0][1];
}
