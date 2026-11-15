# detective
Command-line utility for searching a file for text matching a case-sensitive pattern using a simplified version of the Boyer-Moore string-search algorithm. Inspired by GNU grep.
## Documentation
### Target assessment level
The assessment level target of this work is 3.
### Specification
#### What does the program do?
The program
1. accepts a user-provided text pattern and file path
2. searches for the pattern from the file using the Boyer-Moore-Horspool string search algorithm
3. returns all of the line contents from which the pattern was found, optionally with pattern highlighting and/or line numbers.
#### Data format
The pattern and text file must only contain characters that have a corresponding Unicode code point value less than or equal to 255. Additionally, since each search result only has 1 specified line number, the pattern must not contain any newline characters.
### Correctness
#### Typical test case
File [gpl-3.0.txt](https://github.com/rasmusmiikkulainen/detective/blob/main/gpl-3.0.txt) contains the GPL 3.0 code license. The following is a script obtained when running the program:
```
python main.py LICENSE gpl-3.0.txt
```
#### Algorithms
##### Boyer-Moore string search algorithm (simplified)
This algorithm is used to search a file for the user-specified string pattern. It is not quite a full implementation, since it only implements one of the two parts of the Boyer-Moore, utilizing only the bad-character rule while excluding the good-suffix rule.

The Boyer-Moore algorithm can be significantly faster than naive substring search because it preprocesses the pattern, allowing it to skip multiple characters at a time after a mismatch instead of checking every possible starting position. Preprocessing means transforming data into another form before using that data to perform another operation. In the Boyer-Moore, the algorithm uses a character lookup table created from the pattern, which, in this implementation of the algorithm, is a list with 256 indices each corresponding to one of the Unicode code points (basically an integer representation of a character) 0-255, with index 0 of the table representing the character with Unicode code point 0, index 1 representing code point 1, and so on.

In short, the character lookup table can be thought of as an alphabet, where instead of letters, each index represents a character. Each entry stores the index of that character's last occurence in the pattern, or -1 if the character does not occur in the pattern. So, for example if the pattern was "AbA", the index in the lookup table representing "A" (65) would be set to 2 and the index representing "b" (98) would be set to 1.

After creating this table, the algorithm starts searching for the pattern from the text. The algorithm effectively puts the pattern and an equally long section of the text side-by-side and iterates starting from the last character of the pattern and moving towards the first. When the character in the text and the pattern don't match, the algorithm stops comparing and the text's mismatching character becomes the *bad character*. Next, the algorithm calculates how much it can shift the pattern forward.

The algorithm does this by consulting the generated character lookup table at the index of the bad character's Unicode code point, where it gets either the index of the last occurence of the bad character in the pattern or -1, indicating the absence of that character in the pattern. In the first case, the algorithm shifts the pattern forward so that the last occurence of the bad character in the pattern is lined up with the bad character in the text, or in the case that this would move the pattern backward, shifts the pattern forward by one. In the second case, the algorithm can simply shift the pattern forward until the next search does not include the bad character. Here is an example:
```
Text: ABCBEQXABCDE
Pattern: ABCDE

1.
ABCBEQXABCDE
ABCDE
   ↑

B is now the bad character. Here we shift the pattern so that the last B in pattern matches with the one in the text. Let's calculate the shift:

- index of last occurence of B in pattern: 1
- index of mismatch position relative to pattern: 3
therefore shift = 3 - 1 = 2

2.
ABCBEQXABCDE
  ABCDE
      ↑

Here X is the bad character. Since X is not in the pattern, we can shift the pattern until X is to the left of it. Again, let's calculate the shift:

- index of last occurence of X in pattern: -1
- index of mismatch position relative to pattern: 4
therefore shift = 4 - (-1) = 5

3.
ABCBEQXABCDE
       ABCDE

Match found.
```
#### Lists
Lists in this project are used for:
- storing the character lookup table used by the Boyer-Moore-Horspool algorithm
- storing search results
#### Classes
A class is used to store each search result and provide string formatting options for it via a function.
