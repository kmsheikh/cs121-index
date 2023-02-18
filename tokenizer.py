def tokenize(filePath : str) -> list[str]:
    # read text file and return list of tokens
    # should run in linear time to text file size

    # check input for readability
    f = ""
    try:
        f = open(filePath, "r")
    except:
        print("Couldn't open file ", filePath)
        return False                    # return False if cannot read

    tokens = []
    # read file
    txtfile = f.readlines()
    for text in txtfile:                # process line by line
        text = re.split("\W", text)     # split at non-word characters
        for t in text:                  # add each word to the list
            if len(t) > 0:
                tokens.append(t)
    
    f.close()
    return tokens

def computeWordFrequencies(tokenList : list[str]) -> dict[str, int]:
    # take list of tokens and count # of frequencies as map
    # should run in linear time to text file size
    
    freqMap = {}
    for t in tokenList:             # iterate thru list and count
        if t in freqMap.keys():     # count +1 if already in map
            freqMap[t] += 1
        else:
            freqMap[t] = 1          # start count if not in map
    return freqMap

def printFreq(freqMap : dict[str,int]):
    # display tokens high to low, any ties are displayed in alphanumeric order
    # should run in linear time to text file size

    for f in sorted(list(set(freqMap.values())), reverse=True):     # use set to isolate frequencies then sort as list high to low
        for w in sorted([i for i in freqMap if freqMap[i] == f]):   # iterate through sorted list of tokens with frequency f
            print(f, "=>", w)                                       # print token => frequency