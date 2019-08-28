"""
CS50 pset6 credit
A copy of credit from pset1 implemented in python
Link to info page: https://docs.cs50.net/2019/x/psets/6/sentimental/credit/credit.html
Enda McCarthy - 28/02/19.
"""


import cs50


def main():

    while True:
        ccNumber = cs50.get_int("Enter credit card number: ")
        if ccNumber > 0:
            break

    # gets length of number and also converts number to list of integers
    length = len(str(ccNumber))
    ccNumber = list(str(ccNumber))
    for i in ccNumber:
        i = int(i)

    # ensures only correct lengths are accepted
    if length < 13 or length > 16 or length == 14:
        print("INVALID")
        return

    # start of number validation as per Luhn's algorithm
    list1 = []
    # iterates through the credit card number starting from the end and taking every second value
    # if the value has more than 1 digit it takes the individual digit values
    # appends each result into list1
    for i in range(length - 1, 0, -2):
        temp = int(ccNumber[i - 1]) * 2
        if temp > 9:
            temp1 = temp // 10
            list1.append(temp1)
            temp2 = temp % 10
            list1.append(temp2)
        else:
            list1.append(temp)

    # adds up each value in list1
    list1Total = 0
    for i in list1:
        list1Total = list1Total + i

    # similar process as above
    list2 = []
    for i in range(length, 0, -2):
        temp = int(ccNumber[i - 1])
        list2.append(temp)

    list2Total = 0
    for i in list2:
        list2Total = list2Total + i

    # if Luhn's algorithm is not satisfied then INVALID is outputted
    if ((list1Total + list2Total) % 10) != 0:
        print("INVALID")
        return

    # start of type check
    # only valid numbers make it this far
    if length == 15 and int(ccNumber[0]) == 3 and (int(ccNumber[1]) == 4 or int(ccNumber[1]) == 7):
        print("AMEX")
        return
    elif length == 16 and int(ccNumber[0]) == 5 and int(ccNumber[1]) > 0 and int(ccNumber[1]) < 6:
        print("MASTERCARD")
        return
    elif (length == 13 or length == 16) and int(ccNumber[0]) == 4:
        print("VISA")
        return
    else:
        print("INVALID")
        return


# main function called here
if __name__ == "__main__":
    main()