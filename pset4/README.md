# speller-hash
Harvard CS50 pset4

This is a program designed to spellcheck a text file against a provided dictionary. 
It uses a hashtable (as oppose to a trie) to store each word loaded in from the dictionary. 
It then scans each word in the text file and checks the hashtable to see if it is stored in it.
It also utilises 'getrusage' features in order to obtain the time taken to check the file.
Example command line argument is: ./speller dictionaries/large texts/lalaland.txt (./speller texts/lalaland.txt
will also suffice as a feature is coded in to automatically go to dictionaries/large if nothing is stated.
