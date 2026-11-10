# detective
Command-line utility for searching a file for text matching a pattern using the Boyer-Moore string search algorithm. Inspired by the command `grep` found on Unix-like systems.
## Ideas
- argparse-library for options via cli flags
  - classes could also be used for all the command-line flags (action, description)
    - --help could be a cool use case for this
- algorithms could be further used to sort the search results (lexicographic order, line length)
  - multiple different algorithms could be used
## Documentation
### Target assessment level
The assessment level target of this work is 3.
### Specification
#### What does the program do?
The program
1. reads user input data from a file
2. allows user to search for a specific text pattern from their file
3. returns all of the line numbers as well as the line contents from which the pattern was found.
#### Data format
There is no specified data format as the algorithm works on any text data.
### Correctness
#### Typical test case
foo bar
#### Non-trivial algorithms
##### Boyer-Moore string search algorithm
used to search for the specified string pattern from the larger text
#### Lists
Lists are used to:
- store & return search results
#### Classes
A class is used to store data related to the search result (line number, text) (possibly also for --help?)
