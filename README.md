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
1. accepts a user-provided text pattern and file path
2. searches for the pattern from the file line-by-line using the Boyer-Moore string search algorithm
3. returns all of the line contents from which the pattern was found, optionally with pattern highlighting and/or line numbers.
#### Data format
foo bar
### Correctness
#### Typical test case
foo bar
#### Algorithms used
##### Boyer-Moore string search algorithm
Resources I used:
- https://www.geeksforgeeks.org/dsa/boyer-moore-algorithm-for-pattern-searching/
- https://www.geeksforgeeks.org/dsa/boyer-moore-algorithm-good-suffix-heuristic/
- https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm

This algorithm is used to search a file for the user-specified string pattern. I used the linked documentation as a starting point. However, I deliberately avoided copying code from any existing Python implementation in favor of interpreting the linked text explanations to code. I did, however, need to consult a Python example when implementing the pattern preprocessing step for the bad-character rule.

The algorithm has two main parts, the bad-character rule and the good-suffix rule.
#### Lists
Lists are used for:
- storing the character lookup table used by the Boyer-Moore algorithm
- storing search results
#### Classes
A class is used to store each search result and provide string formatting options for it via a function.
