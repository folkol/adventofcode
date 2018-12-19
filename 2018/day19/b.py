"""Calculate the sum of all divisors of a large number (defined by init part: 17–35).

(For people who are curious of how I ended up with this Python program, see the git history.)

 0 addi 5 16 5		; GOTO 17
 1 seti 1 _ 3		; #3 = 1
 2 seti 1 _ 2		; #2 = 1
 3 mulr 3 2 4		; #4 = #3 * #2
 4 eqrr 4 1 4		; #4 = #4 == #1			| if #4 == #1:
 5 addr 4 5 5		; increase PC with #4	| 	GOTO 7
 6 addi 5 1 5		; GOTO 8				| else: GOTO 8
 7 addr 3 0 0		; #0 += #3
 8 addi 2 1 2		; #2 += 1
 9 gtrr 2 1 4		; #4 = #2 > #1			| if #2 > #1
10 addr 5 4 5		; increase PC with #4	|	GOTO 12
11 seti 2 _ 5		; GOTO 3				| else: GOTO 3
12 addi 3 1 3		; #3 += 1
13 gtrr 3 1 4		; #4 = #3 > #1			| if #3 > #1
14 addr 4 5 5		; increase PC with #4	|	GOTO 16
15 seti 1 _ 5		; GOTO 2				| else: GOTO 2
16 mulr 5 5 5		; GOTO 16*16			| end
17 addi 1 2 1		; #1 += 2
18 mulr 1 1 1		; square #1
19 mulr 5 1 1		; #1 *= 19
20 muli 1 11 1		; #1 *= 11
21 addi 4 1 4		; #4 += 1
22 mulr 4 5 4		; #4 *= 22
23 addi 4 9 4		; #4 += 9
24 addr 1 4 1		; #1 += #4
25 addr 5 0 5		; PC += #0
26 seti 0 _ 5		; GOTO 1
27 setr 5 _ 4		; #4 = 27				| dead code... unless #0 is 1!
28 mulr 4 5 4		; #4 *= 28				|
29 addr 5 4 4		; #4 += 29				|
30 mulr 5 4 4		; #4 *= 30				|
31 muli 4 14 4		; #4 *= 14				|
32 mulr 4 5 4		; #4 *= 32				|
33 addr 1 4 1		; #1 += #4				|
34 seti 0 _ 0		; #0 = 0				|
35 seti 0 _ 5		; GOTO 1				|
"""

# Calculate the sum of all divisors of N, including N.

from math import sqrt

N = 10_551_267
# N = 867

result = 0
skip = sqrt(N)  # Only count factors once, no matter their multiplicity
for i in range(1, int(sqrt(N))):
    if N % i == 0:
        result += i
        if i != skip:
            result += N // i

print(result)
