# colorama is used to add colors to text printed to the terminal

# argparse is used to parse command-line arguments, which are mainly used in
# this project for formatting the data the program prints to the terminal

# pathlib is used to parse file paths

from colorama import Back
import argparse
import pathlib


class SearchResult:
    def __init__(self, line_num, line_content, size, occurences):
        """
        Args:
            line_num (int): line number of the line where the pattern occurs
            line_content (str): contents of the line of text where the pattern occurs
            size (int): length of the pattern
            cases (list): list of indices of line_content where an occurence of pattern starts
        """
        self.line_num = line_num
        self.line_content = line_content
        self.size = size
        self.occurences = occurences

    # here I declare default values for each of the options
    def formatted_result(self, /, numbered=False, hilit=False, only_line_num=False):
        """
        Get a formatted version of the search result.
        Args:
            numbered (bool): whether the resulting string should have the line number
            hilit (bool): whether the pattern should be highlighted in the resulting string
            only_line_num (bool): whether the resulting string should only contain the line number
        Returns:
            string representation of object depending on args
        """
        num = ""
        text = self.line_content

        if numbered:
            num = f"{self.line_num}:  "

        if hilit:
            out = ""
            prev = 0

            for case in self.occurences:
                if case >= prev:
                    out += (
                        text[prev:case]
                        + Back.LIGHTBLACK_EX
                        + text[case : case + self.size]
                        + Back.RESET
                    )
                    prev = case + self.size

            text = out + text[prev:]

        if only_line_num:
            num = ""
            text = str(self.line_num)

        return num + text


def parse_args():
    """
    Parse command-line arguments using argparse.
    """
    parser = argparse.ArgumentParser()
    parser.parse_args()


def prep_badchar(string):
    """
    Get a character lookup table from a given string.
    Args:
        string (str): string to generate the table from
    Returns:
        list with each index representing Unicode code points 0-255
        and each value representing the index of that character's last
        occurence in string, where -1 means the character does not occur.
    """
    out = [-1 for _ in range(256)]

    for i in range(len(string)):
        # ord() returns the Unicode code point (integer representation) of a given character
        # this concept and its significance is further explained in the README

        out[ord(string[i])] = i

    return out


def search(txt, pat):
    """
    Search for a pattern from a text using a simplified version of
    the Boyer-Moore algorithm implemented with only the bad character rule.
    Args:
        txt (str): text to search the pattern from
        pat (str): pattern to be searched from string
    Returns:
        list with the index numbers of each occurence of pat in txt sorted in increasing order
    """
    n = len(txt)
    m = len(pat)

    pat = pat.lower()
    txt = txt.lower()

    if n == 0 or m == 0:
        return []

    char_table = prep_badchar(pat)

    i = 0
    results = []

    while i + m <= n:
        match = True

        for c in reversed(list(enumerate(txt[i : i + m]))):
            rindex = char_table[ord(c[1])]

            if c[1] != pat[c[0]]:
                match = False
                shift = max(1, c[0] - rindex)
                break

        if match:
            results.append(i)
            shift = 1

        i += shift

    return results


def lines_from_file(file_path):
    """
    Get a list of lines in a text file.
    Args:
        file_path (pathlib.Path): file to generate the list from
    Returns:
        list of strings corresponding to lines in the file
    """
    try:
        with open(file_path, "r") as f:
            out = f.read().splitlines()

    except Exception as e:
        print("exception:", e)
        out = []

    return out


testpath = pathlib.Path("gpl-3.0.txt")
pattern = "LICENSE"

results = []
lines = lines_from_file(testpath)
pattern_size = len(pattern)

for i in range(len(lines)):
    line = lines[i]
    line_results = search(line, pattern)
    if line_results:
        results.append(SearchResult(i + 1, line, pattern_size, line_results))

print("\n".join([r.formatted_result(numbered=True, hilit=True) for r in results]))
