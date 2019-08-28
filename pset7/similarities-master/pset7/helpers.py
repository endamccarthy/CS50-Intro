from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # splitlines returns a list of each separate line in a string
    aLines = a.splitlines()
    bLines = b.splitlines()
    result = []
    if len(aLines) >= len(bLines):
        for i in range(len(aLines)):
            repeat = False
            for j in range(len(bLines)):
                if aLines[i] == bLines[j]:
                    for k in range(len(result)):
                        if aLines[i] == result[k]:
                            repeat = True
                    if repeat == False:
                        result.append(aLines[i])
    else:
        for i in range(len(bLines)):
            repeat = False
            for j in range(len(aLines)):
                if bLines[i] == aLines[j]:
                    for k in range(len(result)):
                        if bLines[i] == result[k]:
                            repeat = True
                    if repeat == False:
                        result.append(bLines[i])

    return result


def sentences(a, b):
    """Return sentences in both a and b"""

    # tokenize returns a list of each separate sentence in a string
    aSent = sent_tokenize(a)
    bSent = sent_tokenize(b)
    result = []
    if len(aSent) >= len(bSent):
        for i in range(len(aSent)):
            repeat = False
            for j in range(len(bSent)):
                if aSent[i] == bSent[j]:
                    for k in range(len(result)):
                        if aSent[i] == result[k]:
                            repeat = True
                    if repeat == False:
                        result.append(aSent[i])
    else:
        for i in range(len(bSent)):
            repeat = False
            for j in range(len(aSent)):
                if bSent[i] == aSent[j]:
                    for k in range(len(result)):
                        if bSent[i] == result[k]:
                            repeat = True
                    if repeat == False:
                        result.append(bSent[i])

    return result


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # returns a list with all substrings of length 'num' in string 's'
    def get_substrings(s, num):
        out = []
        if len(s) == num:
            out.append(s)
        elif len(s) > num:
            for i in range(len(s) - num + 1):
                # appends from 'i' up to but not including 'i + num' from string 's' into list 'out'
                out.append(s[i:i + num])
        else:
            return out
        return out

    aSub = get_substrings(a, n)
    bSub = get_substrings(b, n)
    result = []
    if len(aSub) >= len(bSub):
        for i in range(len(aSub)):
            repeat = False
            for j in range(len(bSub)):
                if aSub[i] == bSub[j]:
                    for k in range(len(result)):
                        if aSub[i] == result[k]:
                            repeat = True
                    if repeat == False:
                        result.append(aSub[i])
    else:
        for i in range(len(bSub)):
            repeat = False
            for j in range(len(aSub)):
                if bSub[i] == aSub[j]:
                    for k in range(len(result)):
                        if bSub[i] == result[k]:
                            repeat = True
                    if repeat == False:
                        result.append(bSub[i])

    return result
