"""
CS50 pset6 mario more
A copy of mario more from pset1 implemented in python
Link to info page: https://docs.cs50.net/2019/x/psets/6/sentimental/mario/more/mario.html
Enda McCarthy - 28/02/19.
"""


import cs50


def main():
    while True:
        height = cs50.get_int("Height: ")
        if height > 0 and height < 9:
            break

    for i in range(height):
        print(" " * (height - i - 1) + "#" * (i + 1) + " " * 2 + "#" * (i + 1))


"""
alternative method of getting integer from user without using cs50 library

    while True:
        height = input("Height: ")
        if height.isdigit() == True:
            height = eval(height)
            if height > 0 and height < 9:
                break
"""


# main function called here
if __name__ == "__main__":
    main()