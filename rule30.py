import numpy as np
import time
n = 150
bits = np.ndarray(n)
newbits = bits

def main():
    for i in range(n):
        bits[i] = np.random.randint(0,2)

    k = 100
    for i in range(k):
        loop()
        time.sleep(50/1000)

def loop():
    for i in range(n):
        print("{}".format("." if bits[i] else " "), end='')
        if i == n-1:
            continue
        if not bits[i] and bits[i+1]:
            newbits[i]=1
        elif bits[i] and bits[i-1] and bits[i+1]:
            newbits[i]=0
    print()
    
main()
