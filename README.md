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
$ python main.py -h
usage: python main.py [-h] [-n] [-hi] [-on] pattern filename

command-line file searching tool

positional arguments:
  pattern           pattern to be searched from file
  filename          file to search for pattern

options:
  -h, --help        show this help message and exit
  -n, --numbered    show line numbers
  -hi, --highlight  highlight pattern
  -on, --only-nums  only print line numbers

$ python main.py -on license gpl-3.0.txt
6
10
13
80
81
107
165
222
227
392
395
404
412
416
418
422
430
432
449
458
465
475
484
488
492
495
499
505
507
508
515
517
521
530
534
537
555
584
648
667
674

$ python main.py license gpl-3.0.txt -n -hi
6:   of this license document, but changing it is not allowed.
10:    The GNU General Public License is a free, copyleft license for
13:    The licenses for most software and other practical works are designed
80:    "The Program" refers to any copyrightable work licensed under this
81:  License.  Each licensee is addressed as "you".  "Licensees" and
107:  extent that warranties are provided), that licensees may convey the
165:  convey, without conditions so long as your license otherwise remains
222:      c) You must license the entire work, as a whole, under this
227:      permission to license the work in any other way, but it does not
392:  restriction, you may remove that term.  If a license document contains
395:  of that license document, provided that the further restriction does
404:  form of a separately written license, or stated as exceptions;
412:  this License (including any patent licenses granted under the third
416:  license from a particular copyright holder is reinstated (a)
418:  finally terminates your license, and (b) permanently, if the copyright
422:    Moreover, your license from a particular copyright holder is
430:  licenses of parties who have received copies or rights from you under
432:  reinstated, you do not qualify to receive new licenses for the same
449:  receives a license from the original licensors, to run, modify and
458:  licenses to the work the party's predecessor in interest had or could
465:  not impose a license fee, royalty, or other charge for exercise of
475:  work thus licensed is called the contributor's "contributor version".
484:  patent sublicenses in a manner consistent with the requirements of
488:  patent license under the contributor's essential patent claims, to
492:    In the following three paragraphs, a "patent license" is any express
495:  sue for patent infringement).  To "grant" such a patent license to a
499:    If you convey a covered work, knowingly relying on a patent license,
505:  patent license for this particular work, or (3) arrange, in a manner
507:  license to downstream recipients.  "Knowingly relying" means you have
508:  actual knowledge that, but for the patent license, your conveying the
515:  covered work, and grant a patent license to some of the parties
517:  or convey a specific copy of the covered work, then the patent license
521:    A patent license is "discriminatory" if it does not include within
530:  patent license (a) in connection with copies of the covered work
534:  or that patent license was granted, prior to 28 March 2007.
537:  any implied license or other defenses to infringement that may
555:  permission to link or combine any covered work with a work licensed
584:    Later license versions may give you additional or different
648:      along with this program.  If not, see <https://www.gnu.org/licenses/>.
667:  <https://www.gnu.org/licenses/>.
674:  <https://www.gnu.org/licenses/why-not-lgpl.html>.
```
Running the last command, the program should also highlight occurences of 'license' with a grey background color.
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
