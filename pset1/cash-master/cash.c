#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    // Variables which will be used throughout are declared here initially
    float dollars;
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    
    // Prompt the user to input a value
    // Repeat prompt if conditions are invalid
    do
    {
        dollars = get_float("How much change is owed: ");
    }
    while (dollars <= 0);
    
    // Convert the dollar value to cents. This is to avoid errors when using floats.
    int cents = round(dollars * 100);
    
    // The first line of the following block of code checks if the inputted value can
    // be divided by 25. If so then the total number of quarters is calculated and
    // the result is printed.
    if (cents % quarter == 0)
    {
        int total_quarters = (cents / quarter);
        printf("%i\n", total_quarters);
        return 0;
    }
    
    // This checks if the remainder left after dividing the inputted number by 25
    // is greater than or equal to 10. If not then a check is carried out below to 
    // see if it's greater than or equal to 5. A final else statement then assumes 
    // that it is less than 5.
    else if (cents % quarter >= dime)
    {
        int total_quarters = (cents / quarter);
        int remainder1 = (cents % quarter);
        int total_dimes = (remainder1 / dime);
        int remainder2 = (remainder1 % dime);
        
        if (remainder2 == 0)
        {
            int total2 = total_quarters + total_dimes;
            printf("%i\n", total2);
            return 0;
        }
        else if (remainder2 > nickel)
        {
            int total_nickels = (remainder2 / nickel);
            int remainder3 = (remainder2 % nickel);
            int total_pennies = (remainder3 / penny);
            int total3 = (total_quarters + total_dimes + total_nickels + total_pennies);
            printf("%i\n", total3);
            return 0;
        }
        else if (remainder2 == nickel)
        {
            int total_nickels = (remainder2 / nickel);
            int total4 = (total_quarters + total_dimes + total_nickels);
            printf("%i\n", total4);
            return 0;
        }
        else
        {
            int total_pennies = (remainder2 / penny);
            int total5 = (total_quarters + total_dimes + total_pennies);
            printf("%i\n", total5);
            return 0;
        }
    }
    else if (cents % quarter >= nickel)
    {
        int total_quarters = (cents / quarter);
        int remainder4 = (cents % quarter);
        int total_nickels = (remainder4 / nickel);
        int remainder5 = (remainder4 % nickel);
        
        if (remainder5 == 0)
        {
            int total6 = (total_quarters + total_nickels);
            printf("%i\n", total6);
            return 0;
        }
        else
        {
            int total_pennies = (remainder5 / penny);
            int total7 = (total_quarters + total_nickels + total_pennies);
            printf("%i\n", total7);
            return 0;
        }
    }
    else
    {
        int total_quarters = (cents / quarter);
        int remainder6 = (cents % quarter);
        int total_pennies = (remainder6 / penny);
        int total8 = (total_quarters + total_pennies);
        printf("%i\n", total8);
        return 0;
    }
}
