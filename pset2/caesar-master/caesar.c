#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


string invalid_key = "Usage: ./caesar key\n";

int main(int argc, string argv[])
{
    // argc is the argument count, we want one string after ./caesar so our count will be 2.
    if (argc == 2)
    {
        /* i represents the index of the string in the command line which we want to use for our cipher. 
         * So in this case we always want to use the string that comes after ./caesar which is the 
         * second string, which is at index 1. */
        int i = 1;
        int j;
        int string_length = strlen(argv[i]);
        
        /* This is an array which stores true/false values based on whether each character in the 
         * string is a digit or not. It's length is therefore the same as the string's length. */
        bool digit_check[string_length];
        
        /* This loop checks whether each character in the string is a digit or not. If a character is
         * not a digit it keeps a false value in the corresponding index in the array and vice versa. */
        for (j = 0; j < string_length; j++)
        {
            digit_check[j] = false;
            if (isdigit(argv[i][j]))
            {
                digit_check[j] = true;
            }
        }
       
        /* This loop checks each index in the array. If all the values are true it will repeat 
         * as long as j < string_length. It will then check if j == string_length, if this is the
         * case it will assign a true value (1) to the variable digit_check_true.
         * If any index is false the loop will break and therefore j never gets a chance to equal 
         * string_length. digit_check_true will then be assigned a false value (0). */
        for(j = 0; j < string_length; j++)
        {
            if(!digit_check[j])
            break;
        }    
        int digit_check_true = (j == string_length);
        
        // If any false values were detected in the digit_check array then this will carry out.
        if (digit_check_true == false)
        {
            printf("%s", invalid_key);
            return 1;
        }
        
        // atoi is used to convert from a string to an integer, it is then saved as the key(k).
        int k = atoi(argv[i]);
        
        // Prompts the user for a plaintext message and assigns it's length to l.
        string p = get_string("plaintext:  ");
        int l = strlen(p);
        
        printf("ciphertext: ");
        
        // Iterates through each character of the plaintext message.
        for (j = 0; j < l; j++)
        {
            // Keep case of letter.
            if (isupper(p[j]))
            {
                // Get modulo number and add to appropriate case.
                printf("%c", 65 + ((p[j] - 65 + k) % 26));
            }
            else if (islower(p[j]))
            {
                printf("%c", 97 + ((p[j] - 97 + k) % 26));
            }
            else
            {
                // If the character is not an upper or lower case letter then it remains unchanged.
                printf("%c", p[j]);
            }
        }
        printf("\n");
    }
    else
    {
        printf("%s", invalid_key);
        return 1;
    }
    return 0;
}
