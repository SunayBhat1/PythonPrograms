#Sunay Bhat - ECE 459 Homework
#Caesar Cipher Encryption/Decryption

#Make sure txt file is located in same directory

alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
engLetFreq = [0.080, 0.015, 0.030, 0.040, 0.130, 0.020, 0.015, 0.060, 0.065, 0.005, 0.005, 0.035, 0.030, 0.070, 0.080, 0.020, 0.002, 0.065, 0.060, 0.090, 0.030, 0.010, 0.015, 0.005, 0.020, 0.002]

fName = input("Text File Name (including .txt): ")
mode = input("Encrypt or Decrypt Message (E/D): ")


def encrypt(key):
	with open(fName) as file:
		if mode == 'E' or mode == 'e': print('For key = ' + str(key) + ': '),
		elif mode == 'D' or mode == 'd': print('For key = ' + str(26-key) + ': '),
		while True:
   			c = file.read(1)
   			if not c: 
   				print('\n')
   				break
   			if c == '\n':
   				print(''),
   				continue
   			if c == ' ': 
   				print(' ', end=""),
   				continue
   			ind = alpha.index(c.lower())
   			print(alpha[(ind+key)%26], end=""),

if mode == 'E' or mode == 'e':
	key = int(input("What is the key? (Integer 1-25): "))
	print('')
	encrypt(key)
elif mode == 'D' or mode == 'd':
	freqs = dict()
	fHand = open(fName)
	with open(fName) as file:
		count = 0
		while True:
			c = file.read(1)
			if not c: break
			if c == '\n' or c == ' ': continue
			count += 1
			freqs[c.lower()] = freqs.get(c.lower(),0) + 1
	print('\n1-Gram Letter Frequencies:')
	for i in freqs: print(i + ':', freqs[i])
	table = input("\nDo you want key probability (phi) table? (Y/N): ")
	print('\nPhi Table:')
	keyProbs = list()
	for j in range(0,26):
		summation = 0.0
		for l in freqs:
			summation = ((float(freqs[l])/count) * engLetFreq[alpha.index(l)-j]) + summation
		keyProbs.append(int((summation*100000)+0.5)/100000.0)
	if table == 'Y' or table == 'y': 
		for m in range(len(keyProbs)):  print(str(m) + ':', keyProbs[m])
	numOfKeys = int(input("\nCheck __ most likely keys (integer 1-25): "))
	print('')
	sortKeys = sorted(keyProbs, reverse = True)
	sortKeys = sortKeys[0:numOfKeys]
	for t in sortKeys:
		key = 26 - keyProbs.index(t)
		encrypt(key)
