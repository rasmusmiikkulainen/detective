def bad_char(pattern, string):
    i = 0

    while i + len(pattern) - 1 < len(string):
        test = list(enumerate(zip(pattern, string[i : i + len(pattern)])))
        test.reverse()

        print(i)
        print(test)

        mismatch = False

        for c in test:
            if c[1][0] != c[1][1]:
                bad_char = (c[0], c[1][1])
                mismatch = True
                break

        if not mismatch:
            print("found at index", i)
            # this is wrong
            shift = 1

        else:
            print(bad_char)
            try:
                # index of last occurence of bad_char[1]
                shift = bad_char[0] - pattern.rindex(bad_char[1])
            except ValueError:
                # if bad_char not in pattern, skip
                # this needs to be double-checked
                shift = bad_char[0] + 1
        print(shift, "\n")
        i += shift


t = "AABAACAADAABAABA"
p = "AABA"
bad_char(p, t)
