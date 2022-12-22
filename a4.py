import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	return int( (4* (math.log(26,2)) * m /eps) * (math.log ((2 * (math.log(26,2)) * m /eps),2) ) )

	#I used the 2 claims given in the assignment to calculate the value of N
	#I calculated the probability for all q(prime numbers <= N) for which funtions for pattern and substring in document gives same remainder when divided by q,
	#i.e., (f(p)-f(di))%q=0 , say mod((f(p)-f(di))) = X , we calculate max value of X which comes out to be 26^m -1 , thus, X <= 26^m
	#as given in claim one - the number of prime factors of a positive integer d is at most log(d) (base 2) , so the number of prime factors of X is atmost log(X) ,
	# (base of all log in this explanation is assumed to be 2)
	#as given in claim 2 - let pi(N) denote the number of primes that are less than or equal to N. Then for all N > 1, pi(N) >= N / (2*log(N))
	#Error Probability, Pr is given by number of prime number q's(q<=N) which divides X (say A)/ number of all q's which are less than or equal to N (say B)  (i.e., Pr=A/B)
	#By claim 1 and 2, we have, A<= log(X) and B>= N / (2*log(N)) , which gives , Pr <= (log(26^m) * 2 * log(N) ) / (N) 
	#since greatest upper bound of Pr is eps (/epsilon) we have eps >= (log(26^m) * 2 * log(N)) / (N) 
	#solving this equation (by rearranging first and taking log both side then multiplying by origional equation) we get final result as 
	# N >= 4 * (m/eps) * log(26) * log((2*m/eps)*log(26)) , since we choose q from N, and q is a prime number hence integer so we consider here integer part of equation only

#m=len(p) and n=len(x)
# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):  #O((m+n)logq) tc and O(k+logn+logq) sc
	fxmodq,fpmodq=0,0 
	L=[]
	#we have taken mode before every calculation to restrict value to at max (q-1) which restrict time complexity at O(log(q))
	for i in range (0,len(p)):					#to calculate and store function values(f mod q) for pattern and the initial substring of the document 
		fpmodq=((fpmodq+ ( (((26%q)**(len(p)-i-1))%q) *(((ord(p[i]))-(65))%q) )%q) % q)					#the max value of these expression can be (q-1) since we are taking mod q, provided that for a number n we require log(n) (base 2) bits to store it
		fxmodq=((fxmodq+ ( (((26%q)**(len(p)-i-1))%q) *(((ord(x[i]))-(65))%q) )%q) % q) 					#and the basic arithmetic operations on a b bit number takes bigtheta(b) time ensures that the space complexity to store them is O(log(q)) and 
																			#time complexity to calculate each of them can be atmost O(log(q)+log(q))
		#since loop runs m times time complexity becomes O(m*(log(q)+log(q))) (=t1(say)) and total space complexity becomes O(log(q))

	i=0
	while not (i==len(x)-len(p)+1):						#loop runs until we check for the last possible substring of length m

		#first we check if the function value of substring is same as that of pattern then we update function values and increase index to check for all possible substrings of length m one by one
		if fxmodq==fpmodq:						#for i=0 we have calculated values in above loop, value of fpmodq is fixed
			L.append(i)							#if values matches we report the index in the output

		if i<=len(x)-len(p)-1:							
			fxmodq=( ( (26%q)*(fxmodq- ( (((26%q)**(len(p)-1))%q)*( ((ord(x[i]))-(65)) %q ))) + (( (ord(x[i+len(p)]))-(65) ) %q) ) % q )			#removing calculation for first element of substring and adding for next element that needs to be included
			#since max value can be (q-1) time complexity is O(log(q)),it is updating its value in the previous space only

		i+=1																					#increase index to calculate for next substring, we require space to store this index whose max value can be (n-m+1) ,i.e., log(n-m+1) bits, which requires O(log(n)) space
		#since loop runs (n-m+1) times time complexity becomes O((n-m+1)log(q)) (=t2(say))
	#output list k requires O(k) space as given in assignment
	#Hence, considering all cases including, initialisation,comparison,updation,operations etc. ,we have
	#Total time complexity = t1+t2 = O(m*log(q)+n*log(q)) = O((m+n)*log(q))
	#Total space complexity = O(log(q)+log(n)+k)

	return L

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):		#(m+n)logq tc and k+logn+logq sc
	#here,function definintion changes as I will calculate for all indexes ,for both pattern and substring, except the index at which '?' is present in pattern
	fxmodq, fpmodq=0,0
	L=[]
	spindex=None

	#I have calculated function value for pattern for all indexes except the index at which '?' is present and for initial substring using the same definition explained above
	for i in range (0,len(p)):							

		if p[i]!='?':
			fpmodq=( ( fpmodq+ ( (((26%q)**(len(p)-i-1))%q) * (((ord(p[i]))-(65))%q) )%q ) % q)						#same as explained in above function, time complexity=O(log(q)) and space complexity = O(log(q))
		else:
			spindex=i			#storing index of special character '?' at spindex, space complexity=O(log(m))

		if i!=spindex:
			fxmodq=( ( fxmodq+ ((((26%q)**(len(p)-i-1))%q) * (((ord(x[i]))-(65))%q) )%q ) % q) 					#same as explained in above function, time complexity=O(log(q)) and space complexity = O(log(q))
		#since loop runs m times time complexity becomes O(m*(log(q)+log(q))) (=t1(say)) and total space complexity becomes O(log(q))

	i=0
	j=spindex
	#to calculate and store function values(f mod q) for all possible substrings(length=m) of the document by using the function definition written at the top
	while not (i==len(x)-len(p)+1):							#loop runs until we check for the last possible substring of length m
		
		#first we check if the function value of substring is same as that of pattern then we update function values and increase index to check for all possible substrings of length m one by one
		if fxmodq==fpmodq:
			L.append(i)
		if i<=len(x)-len(p)-1:
			fxmodq=( (fxmodq+ ((((26%q)**(len(p)-spindex-1))%q) * (((ord(x[j]))-(65))%q) )%q ) % q)				#adding for the index which we left in last calculation,i.e, for substring of length m element at index spindex
			j+=1																		#pointer that keep track of spindex in substring of length m,its max value can be (m-1)+(n-m+1)=n, which requires O(log(n)) space					
			fxmodq=( ((((26%q)*((fxmodq- ( (((26%q)**(len(p)-1))%q) * (((ord(x[i]))-(65))%q) )%q)%q))%q)+ (((ord(x[i+len(p)]))-(65))%q) - (( (((26%q)**(len(p)-spindex-1))%q) * (((ord(x[j]))-(65))%q) ) %q) ) % q )	#removing calculation for first element of substring and adding for next element that needs to be included then subtracting for spindex element
			#since max value can be (q-1) time complexity is O(log(q)),it is updating its value in the previous space only
		i+=1											#increase index to calculate for next substring, we require space to store this index whose max value can be (n-m+1) ,i.e., log(n-m+1) bits, which requires O(log(n)) space
		#since loop runs (n-m+1) times time complexity becomes O((n-m+1)log(q)) (=t2(say))
	#output list k requires O(k) space as given in assignment
	#Hence,considering all cases including, initialisation,comparison,updation,operations etc. ,we have
	#Total time complexity = t1+t2 = O(m*log(q)+n*log(q)) = O((m+n)*log(q))
	#Total space complexity = O(log(q)+log(n)+k)

	return L
