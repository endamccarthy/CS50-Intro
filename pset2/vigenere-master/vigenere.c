#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// This is the prototype for the function used to convert the alphabetic key into a numeric key.
int shift(char c);

string invalid_key = "Usage: ./vigenere keyword\n";

int main(int argc, string argv[])
{
    // argc is the argument count, we want one string after ./vigenere so our count will be 2.
    if (argc == 2)
    {
        /* i represents the index of the string in the command line which we want to use for our cipher. 
         * So in this case we always want to use the string that comes after ./vigenere which is the 
         * second string, which is at index 1. */
        int i = 1;
        int j;
        int string_length = strlen(argv[i]);
        
        /* This is an array which stores true/false values based on whether each character in the 
         * string is an alphabetic letter or not. It's length is therefore the same as the string's length. */
        bool alpha_check[string_length];
        
        /* This loop checks whether each character in the string is an alphabetic letter or not. If a character
         * is not a letter it keeps a false value in the corresponding index in the array and vice versa. */
        for (j = 0; j < string_length; j++)
        {
            alpha_check[j] = false;
            if (isalpha(argv[i][j]))
            {
                alpha_check[j] = true;
            }
        }
       
        /* This loop checks each index in the array. If all the values are true it will repeat 
         * as long as j < string_length. It will then check if j == string_length, if this is the
         * case it will assign a true value (1) to the variable alpha_check_true.
         * If any index is false the loop will break and therefore j never gets a chance to equal 
         * string_length. alpha_check_true will then be assigned a false value (0). */
        for (j = 0; j < string_length; j++)
        {
            if (!alpha_check[j])
            {
                break;
            }
        }    
        int alpha_check_true = (j == string_length);
        
        // If any false values were detected in the alpha_check array then this will carry out.
        if (alpha_check_true == false)
        {
            printf("%s", invalid_key);
            return 1;
        }
        
        // Prompts the user for a plaintext message and assigns it's length to l.
        string p = get_string("plaintext:  ");
        int l = strlen(p);
        
        printf("ciphertext: ");
        
        // This variable will be used to count each time a non alphabetic character is found in p.
        int non_alpha = 0;
        
        // Iterates through each character of the plaintext message.
        for (j = 0; j < l; j++)
        {
            // k will be used as the key. 
            int k;
            if (j < string_length)
            {
                k = shift(argv[i][j - non_alpha]);
            }
            else
            {
                /* Using the modulus ensures that if the length of the keyword is less than
                 * the length of the 'plaintext' message, the keyword will be looped back to the 
                 * first character once it reaches the end. The non_alpha value is used to make 
                 * sure that the keyword will ignore non alphabetic characters (for example, if the 
                 * keyword is 'abc' and the message is 'Hi! Joe', the H will rotate 'a' times, the i
                 * will rotate 'b' times and the J will rotate 'c' times.). */
                int mod = ((j - non_alpha) % string_length);
                k = shift(argv[i][mod]);
            }
            
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
                non_alpha++;
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

// Definition of shift function.
int shift(char c)
{
    int out;
    if (isupper(c))
    {
        out = c - 'A';
    }
    else
    {
        out = c - 'a';
    }
    return out;
}
