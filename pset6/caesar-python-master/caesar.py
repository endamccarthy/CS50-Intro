"""
CS50 pset6 caesar
A copy of caesar from pset2 implemented in python
Link to info page: https://docs.cs50.net/2019/x/psets/6/sentimental/caesar/caesar.html
Enda McCarthy - 28/02/19.
"""

import cs50
import sys


def main():
    invalidkey = "Usage: python caesar.py k"
    if len(sys.argv) != 2:
        print(invalidkey)
        # error handling
        sys.exit(1)

    # converts key to a number between 0-26
    if int(sys.argv[1]) < 26:
        k = int(sys.argv[1])
    else:
        k = int(sys.argv[1]) % 26

    # rotates each plaintext letter through given key and prints ciphertext output one letter at a time
    p = cs50.get_string("plaintext:  ")
    print("ciphertext: ", end="")
    for char in p:
        if char.isalpha() and char.isupper():
            num = ((ord(char) - 65 + k) % 26) + 65
            print(chr(num), end="")
        elif char.isalpha() and char.islower():
            num = ((ord(char) - 97 + k) % 26) + 97
            print(chr(num), end="")
        else:
            print(char, end="")
    print()


# main function called here
if __name__ == "__main__":
    main()
