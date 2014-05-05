#!/usr/bin/python

def special(lst):
    ones = 0
    twos = 0
    for x in lst:
      twos |= ones & x
      ones ^= x
      not_threes = ~(ones & twos)
      ones &= not_threes
      twos &= not_threes
    
    return ones

if __name__ == "__main__":
#    lst = [1, 2, 4, 6, 4, 1, 2, 3, 6, 4, 2, 1, 3, 6]
    lst = [4, 5, 4]
    print special(lst)

