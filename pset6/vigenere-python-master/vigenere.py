"""
CS50 pset6 vigenere
A copy of vigenere from pset2 implemented in python
Link to info page: https://docs.cs50.net/2019/x/psets/6/sentimental/vigenere/vigenere.html
Enda McCarthy - 01/03/19.
"""

import cs50
import sys


def main():
    invalidkey = "Usage: ./vigenere keyword"
    if len(sys.argv) != 2 or sys.argv[1].isalpha() != True:
        print(invalidkey)
        # error handling
        sys.exit(1)

    # creates list to store numeric values (0-26) of each keyword character
    kNum = []
    for i in sys.argv[1]:
        if i.isupper():
            kNum.append(ord(i) - 65)
        else:
            kNum.append(ord(i) - 97)

    p = cs50.get_string("plaintext:  ")
    print("ciphertext: ", end="")

    # n is a counter which ensures that the keyword is not affected by non-alpha characters
    n = 0
    for char in p:
        # loops keyword back to start if end is reached
        if n == len(str(sys.argv[1])):
            n = 0
        if char.isalpha() and char.isupper():
            # modulus is used to wrap around from Z back to A
            num = ((ord(char) - 65 + kNum[n]) % 26) + 65
            n += 1
            print(chr(num), end="")
        elif char.isalpha() and char.islower():
            num = ((ord(char) - 97 + kNum[n]) % 26) + 97
            n += 1
            print(chr(num), end="")
        else:
            print(char, end="")
    print()


# main function called here
if __name__ == "__main__":
    main()