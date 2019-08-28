#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Height variable declared initially
    int height;
    
    // Prompt the user to input a height value and repeat prompt if conditions are invalid
    do
    {
       height = get_int("Input pyramid height (between 1-8): ");
    }
    while (height < 1 || height > 8);
    
    // The following loop will occur for each row
    for (int row = 1; row <= height; row++)
    {
        // Prints the required number of spaces on each row depending on the inputted height
        for (int space = row; space <= height - 1; space++)
        {
            printf(" ");
        }
        
        // Prints the required number of hashes on each row depending on the inputted height
        for (int hash = 1; hash <= row; hash++)
        {
            printf("#");
        }
        
        // Moves onto the next row
        printf("\n");
    }
}
