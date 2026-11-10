from colorama import Back


class SearchResult:
    def __init__(self, line_content, pattern):
        self.pattern = pattern
        self.line_content = line_content

    def set_line_num(self, line_num):
        self.line_num = line_num

    def formatted_str(self, /, numbered, hilit):
        num = ""
        text = self.line_content
        if numbered:
            num = f"{self.line_num}:  "
        if hilit:
            text = text.replace(self.pattern, Back.LIGHTBLACK_EX + self.pattern + Back.RESET)
        return num + text

    def __str__(self):
        return self.line_content


def preprocess_string(string):
    out = [-1 for _ in range(256)]

    for i in range(len(string)):
        out[ord(string[i])] = i

    return out


def search(txt, pat):
    n = len(txt)
    m = len(pat)

    bad_char = preprocess_string(pat)

    i = 0
    results = []

    while i + m <= n:
        mismatch = False
        for c in reversed(list(enumerate(txt[i : i + m]))):
            rindex = bad_char[ord(c[1])]

            if rindex == -1 or c[1] != pat[c[0]]:
                if rindex == -1:
                    shift = c[0] + 1
                elif c[1] != pat[c[0]]:
                    shift = max(1, c[0] - rindex)
                mismatch = True
                break

        if not mismatch:
            results.append(i)
            shift = 1

        i += shift

    return results


t = "AABAACAADAABAABA"
p = "AABA"

print(search(t, p))
