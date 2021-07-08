 

n = int(input("Enter n number of values available: "))
k = int(input("Enter k number of values to choose: "))
#rep = char(input("Are repetitions allowed? (Y/N): "))

m = n - k
num = n
denom = 1

if k >= m:
	for nVal in range(k+1,n):
		num = num * nVal
	for dVal in range (2,m+1):
		denom = denom * dVal
	answer = num / denom
	print ('Answer: ', answer)
elif m > k:
	for nVal in range(m+1,n):
		num = num * nVal
	for dVal in range (2,k+1):
		denom = denom * dVal
	answer = num / denom
	print ('Answer: ', answer)
