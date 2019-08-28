"""
CS50 pset6 cash
A copy of cash from pset1 implemented in python
Link to info page: https://docs.cs50.net/2019/x/psets/6/sentimental/cash/cash.html
Enda McCarthy - 28/02/19.
"""


import cs50


def main():
    while True:
        dollars = cs50.get_float("How much change is owed: ")
        if dollars > 0:
            break

    cents = round(dollars * 100)
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1

    if cents % quarter == 0:
        totalQuarters = cents // quarter
        print(int(totalQuarters))
        return

    elif cents % quarter >= dime:
        totalQuarters = cents // quarter
        remainder1 = cents % quarter
        totalDimes = remainder1 // dime
        remainder2 = remainder1 % dime
        if remainder2 == 0:
            total1 = totalQuarters + totalDimes
            print(int(total1))
            return
        elif remainder2 > nickel:
            totalNickels = remainder2 // nickel
            remainder3 = remainder2 % nickel
            totalPennies = remainder3 // penny
            total2 = totalQuarters + totalDimes + totalNickels + totalPennies
            print(int(total2))
            return
        elif remainder2 == nickel:
            totalNickels = remainder2 // nickel
            total3 = totalQuarters + totalDimes + totalNickels
            print(int(total3))
            return
        else:
            totalPennies = remainder2 // penny
            total4 = totalQuarters + totalDimes + totalPennies
            print(int(total4))
            return

    elif cents % quarter >= nickel:
        totalQuarters = cents // quarter
        remainder4 = cents % quarter
        totalNickels = remainder4 // nickel
        remainder5 = remainder4 % nickel
        if remainder5 == 0:
            total5 = totalQuarters + totalNickels
            print(int(total5))
            return
        else:
            totalPennies = remainder5 // penny
            total6 = totalQuarters + totalNickels + totalPennies
            print(int(total6))
            return

    else:
        totalQuarters = cents // quarter
        remainder6 = cents % quarter
        totalPennies = remainder6 // penny
        total7 = totalQuarters + totalPennies
        print(int(total7))
        return


# main function called here
if __name__ == "__main__":
    main()