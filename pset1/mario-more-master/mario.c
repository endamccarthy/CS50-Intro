#include <cs50.h>
#include <stdio.h>

// Declares a function called hashes and an integer called row within the argument
// The function can be called numerous times within the main program
// This elimates the need to write out the hashes instruction twice in the program
// This is an example of abstraction
void hashes(int row);

// This is the definition of the hashes function
// Because row is used within it, it needs to be declared in the argument
// This was done at the start of the program when the function was declared
// row can then be used throughout the program
void hashes(int row)
{
    for (int hash = 1; hash <= row; hash++)
    {
         printf("#");
    }
}

int main(void)
{
    // Height variable declared initially
    int height;
  
    // Prompt the user to input a height value
    // Repeat prompt if conditions are invalid
    do
    {
        height = get_int("Input pyramid height (between 1-8): ");
    }
    while (height < 1 || height > 8);
    
    // The following loop will occur for each row
    for (int row = 1; row <= height; row++)
    {
        // Prints the required number of spaces at the start of each row
        for (int space = row; space <= height - 1; space++)
        {
            printf(" ");
        }
        
        // Prints the required number of hashes on the lhs of each row
        // See definition at the start of the program
        // The function requires row in the argument as per the definition
        hashes(row);
        
        // Prints 2 spaces in the middle of the pyramid
        printf("  ");
        
        // Prints the required number of hashes on the rhs of each row
        hashes(row);
        
        // Moves onto the next row
        printf("\n");
    }
}
