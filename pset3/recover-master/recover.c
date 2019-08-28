// CS50 pset3 recover
// A program to recover deleted JPEG images from a source file.
// Link to info page: https://docs.cs50.net/2019/x/psets/3/recover/recover.html#background
// Enda McCarthy - 07/02/19.


#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filename
    char *image = argv[1];

    // open input file
    FILE *inptr = fopen(image, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", image);
        return 2;
    }


    int a, n = 0;

    /* Declares the buffer pointer outside of the main loop. Making it an unsigned char means it will
       read the hexadecimal values which are stored in each byte of the source file.
       A pointer to a file is also declared, this is used to create each .jpg file. */
    unsigned char *buffer;
    FILE *img;

    /* This is the main loop. It reads blocks of 512 bytes from the source file. It checks the first 4 bytes
       of each block. If these match those of a JPEG signature it will create a new .jpg file, name it, open it and write
       the associated block to it, otherwise it moves onto the next block. If the next block has no signature but a .jpg
       file is already open it will write the block to that .jpg. Once it reaches the start of a new JPEG it will close
       the old .jpg file and repeat the above. This continues until it reaches the EOF. */
    while (1)
    {
        buffer = (unsigned char *) malloc(512);  // Allocates 512 bytes of memory to buffer.

        // Reads a block of 512 bytes and checks for EOF at the same time.
        if ((fread(buffer, 1, 512, inptr)) < 512)
        {
            if (a == 2)
            {
                fclose(img);  // If a == 2 it means there is a file open.
            }
            break;
            return 0;
        }

        // Checks the first 4 bytes for a JPEG signature.
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            if (a == 2)
            {
                fclose(img);  // If a == 2 it means there is a previous file open.
            }
            a = 1;  // Indicates the start of a new JPEG, used below.
        }

        // If a == 2 it means there is already a file open, the block will be added to it.
        if (a == 2)
        {
            fwrite(buffer, 1, 512, img);
        }

        // New .jpg file created, named, opened and written to.
        if (a == 1)
        {
            char filename[7];
            sprintf(filename, "%03i.jpg", n);
            n++;
            img = fopen(filename, "w");
            fwrite(buffer, 1, 512, img);
            a = 2;
        }
    }

    // free allocated memory
    free(buffer);

    // close infile
    fclose(inptr);

    // success
    return 0;
}


