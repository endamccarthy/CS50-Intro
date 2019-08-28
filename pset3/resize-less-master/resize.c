// CS50 pset3 resize less
// A program to scale up an image by a user inputted factor between 0-100
// Link to info page: https://docs.cs50.net/2019/x/psets/3/resize/less/resize.html
// Enda McCarthy - 04/02/19.

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "bmp.h"


int main(int argc, char *argv[])
{
    int i, j, k, l, m;
    int n = atoi(argv[1]);    // converts string to digits.
    int numberLength = strlen(argv[1]);
    int checkArray[numberLength];    // declares temp array to store values based on the string being digits or not.

    /* iterates through each character of the second command line argument and stores a 0/1 value in checkArray
       based on weather the character is a digit or not. */
    for (i = 0; i < numberLength; i++)
    {
        checkArray[i] = 0;
        bool digit = isdigit(argv[1][i]);
        if (digit == true)
        {
            checkArray[i] = 1;
        }
    }

    /* checks each value in checkArray. if a value is 0 (not a digit) then it breaks and digitTrue is false. if all
       values are 1 then i will equal numberLength and digitTrue is true. */
    for (i = 0; i < numberLength; i++)
    {
        if (checkArray[i] == 0)
        {
            break;
        }
    }
    bool digitTrue = (i == numberLength);


    // check if the filetype is correct.
    char filetype[] = ".bmp";
    char *ptr;    // declares a pointer variable which will be used below.
    for (i = 2; i < 4; i++)    // iterate through the third and fourth command line arguments.
    {
        int filenameLength = strlen(argv[i]);
        // initializes ptr to point to the address of the fourth last character in the relative command line argument.
        ptr = &argv[i][filenameLength - 4];
        j = 0;

        /* can also be written as 'while (*ptr != '\0')'. basically it loops through each character of ptr until it
           hits the NULL (ptr++ increments the address each time). the * means it looks at the actual value that is
           inside the address. it checks if the character matches the corresponding character in filetype and breaks
           if it does not. */
        while (*ptr)
        {
            if (*ptr != filetype[j])
            {
                break;
            }
            ptr++;
            j++;
        }

        if (j != 4)    // j will equal to 4 if all the characters are matched.
        {
            break;
        }
    }

    // ensure proper usage
    if (argc != 4 || digitTrue != true || n <= 0 || n > 100 || j != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }


    // remember filenames.
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file.
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file.
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // remember infiles values which will be used further on
    int a = abs(bi.biHeight);
    int b = bi.biWidth;
    int paddingOld = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // multiply the height and width by a factor of n.
    bi.biHeight *= n;
    bi.biWidth *= n;
    // determine padding for scanlines
    int paddingNew = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    bi.biSizeImage = ((bi.biWidth * 3) + paddingNew) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // iterate over infile's scanlines
    for (i = 0; i < a; i++)
    {
        // repeat the 'scanning' and 'writing' of each scanline n times.
        for (j = 0; j < n; j++)
        {
            // iterate over pixels in scanline
            for (k = 0; k < b; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for (l = 0; l < n; l++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);    // write RGB triple to outfile
                }
            }

            // put cursor back to start of infiles scanline
            fseek(inptr, (b * -3), SEEK_CUR);

            // add padding to end of each scanline in outfile
            for (m = 0; m < paddingNew;  m++)
            {
                fputc(0x00, outptr);
            }
        }
        // skip over padding, if any
        fseek(inptr, ((b * 3) + paddingOld), SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
