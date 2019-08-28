// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node* next;
}
node;

// Represents a hash table
node *hashtable[N];

unsigned int wordCount = 0;

bool loaded = false;

// Hashes word to a number between 0 and N
// Taken from: https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
unsigned int hash(const char* word)
 {
     unsigned long hash = 5381;
     for (const char* c = word; *c != '\0'; c++)
     {
         hash = ((hash << 5) + hash) + tolower(*c);
     }
     return hash % N;
 }


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hashCode = hash(word);
    // Sets a cursor to the appropriate index in the hashtable array (this index then points to a linked list)
    node* cursor = hashtable[hashCode];

    if (cursor == NULL)
    {
        return false;
    }
    else if (cursor != NULL)
    {
        // check associated linked list for the word
        while (cursor != NULL)
        {
            // strcasecmp ignores the case of the words being compared
            if (strcasecmp(cursor->word, word) == 0)
            {
                return true;
            }
            else
            {
                cursor = cursor->next;
            }
        }
    }
    return false;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Insert words into hash table
    while (true)
    {
        // Allocate memory for each new word
        node *ptr = malloc(sizeof(node));
        // Check that enough memory is available
        if (ptr == NULL)
        {
            return false;
        }

        // Scans a word from the dictionary and saves it to ptr->word
        fscanf(file, "%s", ptr->word);
        ptr->next = NULL;
        if (feof(file))
        {
            free(ptr);
            break;
        }

        wordCount++;
        int hashCode = hash(ptr->word);

        // If the index already has a linked list, the new ptr is slotted in at the start of the list
        if (hashtable[hashCode] != NULL)
        {
            ptr->next = hashtable[hashCode];
        }
        // Assigns the up to date list back to the correct index
        hashtable[hashCode] = ptr;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    loaded = true;
    return true;
}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
        return wordCount;
    }
    return 0;
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Iterated through each index of the hashtable freeing each node of the linked lists
    for (int i = 0; i < N; i++)
    {
        node *cursor1 = hashtable[i];
        while (cursor1 != NULL)
        {
            node* temp = cursor1;
            cursor1 = cursor1->next;
            free(temp);
        }
    }
    loaded = false;
    return true;
}
