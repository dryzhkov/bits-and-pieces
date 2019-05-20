def NOR(x, y):
    if x == 0 and y == 0:
        return 1
    elif x == 1 and y == 0:
        return 0
    elif x == 0 and y == 1:
        return 0
    else:  # both are 1
        return 0


def NOT(x):
    return NOR(x, 0)


def OR(x, y):
    return NOT(NOR(x, y))


def AND(x, y):
    return NOT(OR(NOT(x), NOT(y)))


def XOR(x, y):
    return AND(OR(x, y), NOT(AND(x, y)))


"""Half-adder
    Given input bits x and y returns the sum bit and carry over

    inputs (x and y)	carry	sum
    0 + 0	                0	0
    0 + 1	                0	1
    1 + 0	                0	1
    1 + 1	                1	0
"""


def HALF(x, y):
    sum = XOR(x, y)
    carry = AND(x, y)
    return (sum, carry)


"""Full-adder
    Accept 2 bits (x and y) and a carry over bit, computes sum and carry out bit

    x	y	carry_in	carry_out	sum
    0	0	    0	        0	    0
    0	1	    0	        0	    1
    1	0	    0	        0	    1
    1	1	    0	        1	    0
    0	0	    1	        0	    1
    0	1	    1	        1	    0
    1	0	    1	        1	    0
    1	1	    1	        1	    1
"""


def FULL(x, y, carry_in):
    sum1, carry1 = HALF(x, y)
    sum2, carry2 = HALF(sum1, carry_in)
    carry_out = OR(carry1, carry2)
    return (sum2, carry_out)


"""Add 2 4 bit integers using logic simple logic gates"""


def ADD4(left, right):
    sum3, carry3 = FULL(left[3], right[3], 0)
    sum2, carry2 = FULL(left[2], right[2], carry3)
    sum1, carry1 = FULL(left[1], right[1], carry2)
    sum0, _ = FULL(left[0], right[0], carry1)
    return [sum0, sum1, sum2, sum3]
